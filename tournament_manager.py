import sqlite3
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tournament")

DB_PATH = "tournament.db"

import subprocess
import json
import random
import glob

# ... (keep existing imports) ...

class TournamentManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    command TEXT NOT NULL,
                    rating REAL DEFAULT 1200.0,
                    is_active INTEGER DEFAULT 1
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    map_path TEXT,
                    timestamp REAL,
                    replay_path TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS match_participants (
                    match_id INTEGER,
                    player_id INTEGER,
                    rank INTEGER,
                    score INTEGER,
                    status TEXT,
                    FOREIGN KEY(match_id) REFERENCES matches(id),
                    FOREIGN KEY(player_id) REFERENCES players(id)
                )
            """)
            conn.commit()
        logger.info(f"Database {self.db_path} initialized.")

    def add_player(self, name, command):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO players (name, command) VALUES (?, ?)", (name, command))
            cursor.execute("UPDATE players SET command = ?, is_active = 1 WHERE name = ?", (command, name))
            conn.commit()

    def get_active_players(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_leaderboard(self):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name, rating FROM players WHERE is_active = 1 ORDER BY rating DESC")
            return [dict(row) for row in cursor.fetchall()]

    def update_elo(self, participants):
        """
        participants: list of dicts {player_id, rank}
        For simplicity, we treat a multi-player game as a series of 1v1 interactions.
        """
        k = 10
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Fetch current ratings
            ratings = {}
            for p in participants:
                cursor.execute("SELECT rating FROM players WHERE id = ?", (p['player_id'],))
                ratings[p['player_id']] = cursor.fetchone()[0]

            new_ratings = ratings.copy()

            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    p1 = participants[i]
                    p2 = participants[j]
                    
                    id1, id2 = p1['player_id'], p2['player_id']
                    r1, r2 = ratings[id1], ratings[id2]
                    
                    e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
                    e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))
                    
                    # s = 1 for win, 0.5 for draw, 0 for loss
                    if p1['rank'] < p2['rank']:
                        s1, s2 = 1, 0
                    elif p1['rank'] > p2['rank']:
                        s1, s2 = 0, 1
                    else:
                        s1, s2 = 0.5, 0.5
                        
                    new_ratings[id1] += k * (s1 - e1) / (len(participants) - 1)
                    new_ratings[id2] += k * (s2 - e2) / (len(participants) - 1)

            for pid, val in new_ratings.items():
                cursor.execute("UPDATE players SET rating = ? WHERE id = ?", (val, pid))
            conn.commit()

    def run_match(self, player_ids, map_path):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            players = []
            for pid in player_ids:
                cursor.execute("SELECT * FROM players WHERE id = ?", (pid,))
                players.append(dict(cursor.fetchone()))

        bot_cmds = [p['command'] for p in players]
        
        # Store match (initial)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO matches (map_path, timestamp) VALUES (?, ?)", (map_path, time.time()))
            match_id = cursor.lastrowid
            conn.commit()

        # Build playgame.py command
        replay_filename = f"{match_id}.replay"
        player_names = ",".join([p['name'] for p in players])
        cmd = [
            "python3", "engine/playgame.py",
            "--map_file", map_path,
            "--log_dir", "replays",
            "--log_replay",
            "--log_stdout",
            "--turns", "500",
            "--serial",
            "--game", str(match_id),
            "--player_names", player_names
        ] + bot_cmds

        logger.info(f"Starting match {match_id}: {' vs '.join([p['name'] for p in players])} on {map_path}")
        
        try:
            result_process = subprocess.run(cmd, capture_output=True, text=True)
            if result_process.returncode != 0:
                logger.error(f"Engine failed: {result_process.stderr}")
                return None
            
            # Find the JSON line in output
            lines = result_process.stdout.splitlines()
            result_json = None
            for line in reversed(lines):
                if line.startswith('{'):
                    result_json = json.loads(line)
                    break
            
            if not result_json:
                logger.error("No result JSON found in engine output")
                return None

            # Update match with results and participants
            replay_path = os.path.join("replays", replay_filename)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE matches SET replay_path = ? WHERE id = ?", (replay_path, match_id))
                
                participants_data = []
                for i, pid in enumerate(player_ids):
                    p_rank = result_json['rank'][i]
                    p_score = result_json['score'][i]
                    p_status = result_json['status'][i]
                    
                    cursor.execute("""
                        INSERT INTO match_participants (match_id, player_id, rank, score, status)
                        VALUES (?, ?, ?, ?, ?)
                    """, (match_id, pid, p_rank, p_score, p_status))
                    
                    participants_data.append({'player_id': pid, 'rank': p_rank})
                
                conn.commit()
            
            # Update ELO
            self.update_elo(participants_data)
            logger.info(f"Match {match_id} finished and ratings updated.")
            return result_json

        except Exception as e:
            logger.error(f"Error running match: {e}")
            return None

if __name__ == "__main__":
    db = TournamentManager()
    print("Database initialized successfully.")
