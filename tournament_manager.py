import sqlite3
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tournament")

DB_PATH = "tournament.db"

class TournamentDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    command TEXT NOT NULL,
                    rating REAL DEFAULT 1200.0,
                    is_active INTEGER DEFAULT 1
                )
            """)
            # Matches table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    map_path TEXT,
                    timestamp REAL,
                    replay_path TEXT
                )
            """)
            # Participants table (for multi-player support)
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
            cursor.execute("""
                INSERT OR IGNORE INTO players (name, command) VALUES (?, ?)
            """, (name, command))
            cursor.execute("""
                UPDATE players SET command = ?, is_active = 1 WHERE name = ?
            """, (command, name))
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
            cursor.execute("SELECT name, rating FROM players ORDER BY rating DESC")
            return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    db = TournamentDB()
    print("Database initialized successfully.")
