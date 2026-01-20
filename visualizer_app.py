import os
import sqlite3
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tournament_manager import TournamentManager, DB_PATH

app = FastAPI(title="Ants AI Tournament")
app.mount("/visualizer", StaticFiles(directory="engine/visualizer"), name="visualizer")
app.mount("/replays", StaticFiles(directory="replays"), name="replays")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    tm = TournamentManager()
    leaderboard = tm.get_leaderboard()
    
    # Fetch recent matches with participants
    matches = []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM matches ORDER BY timestamp DESC LIMIT 20")
        match_rows = cursor.fetchall()
        
        for m in match_rows:
            match_id = m['id']
            cursor.execute("""
                SELECT p.name, mp.rank, mp.score, mp.status
                FROM match_participants mp
                JOIN players p ON mp.player_id = p.id
                WHERE mp.match_id = ?
                ORDER BY mp.rank ASC
            """, (match_id,))
            participants = [dict(p) for p in cursor.fetchall()]
            
            match_data = dict(m)
            match_data['participants'] = participants
            match_data['dt_str'] = datetime.fromtimestamp(m['timestamp']).strftime('%Y-%m-%d %H:%M')
            matches.append(match_data)
            
    return templates.TemplateResponse("index.html", {
        "request": request,
        "leaderboard": leaderboard,
        "matches": matches
    })

@app.get("/replay/{match_id}", response_class=HTMLResponse)
async def replay(match_id: int):
    # Fetch replay_path from DB
    replay_path = None
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT replay_path FROM matches WHERE id = ?", (match_id,))
        row = cursor.fetchone()
        if row:
            replay_path = row['replay_path']

    if not replay_path or not os.path.exists(replay_path):
        return HTMLResponse(f"Replay file for match {match_id} not found.", status_code=404)

    with open(replay_path, "r") as f:
        replay_data = f.read()

    # Load template
    template_path = "engine/visualizer/replay.html.template"
    with open(template_path, "r") as f:
        content = f.read()

    # Apply placeholders
    content = content.replace("## PATH PLACEHOLDER ##", "/visualizer/")
    
    # Replay data needs escaping for JS string
    escaped_data = replay_data.replace("'", "\'" ).replace("\n", "")
    content = content.replace("## REPLAY PLACEHOLDER ##", escaped_data)

    return HTMLResponse(content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
