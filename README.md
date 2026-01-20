# Ants AI Tournament Platform 🐜

A comprehensive platform for developing, testing, and running tournaments for AI bots based on the Google AI Challenge "Ants" engine. This project provides a full-stack environment including an execution engine, a tournament manager with ELO rating system, and a web-based visualizer.

---

## 🌟 Features

- **Multi-Bot Support**: Support for bots written in Python, C++, Java, Go, and more.
- **Automated Tournament**: A background worker that picks random maps and bots to run matches continuously.
- **ELO Rating System**: Automatic skill estimation for every bot based on match results.
- **Web Dashboard**: 
  - Real-time Leaderboard.
  - Recent Match History.
  - Built-in Replay Visualizer (watch matches directly in your browser).
- **Dockerized Environment**: One-command setup for the entire infrastructure.
- **Improved Naming**: Bots are identified by their registered names (e.g., `ExplorerBot`) rather than generic filenames.

---

## 🏗 System Architecture

The project is divided into three main components:

1.  **Tournament Worker**: Orchestrates matches, selects maps/players, and updates the SQLite database.
2.  **Game Engine**: The core logic (forked from the original competition) that simulates the ants' world and enforces rules.
3.  **Visualizer App**: A FastAPI web server that provides the dashboard and serves the HTML5 replay tool.

---

## 🚀 Quick Start (Docker)

The easiest way to run the tournament and see your bots in action.

### 1. Requirements
- **Docker** and **Docker Compose** installed.

### 2. Launch the Platform
```bash
docker-compose up -d --build
```

### 3. Access the Dashboard
Open [http://localhost:8000](http://localhost:8000) in your browser. You will see the leaderboard and matches as they are being played.

---

## 🤖 Bot Development

### How to add your own bot
1. Create a new directory in `bots/` (e.g., `bots/my_super_bot/`).
2. Implement your logic in a file (e.g., `MyBot.py`). You can use existing bots as templates.
3. Open `register_new_bots.py` and add your bot to the `bots` dictionary:
   ```python
   "MySuperBot": "python3 bots/my_super_bot/MyBot.py"
   ```
4. Restart the containers:
   ```bash
   docker-compose restart tournament
   ```
   *Note: The tournament worker automatically registers new bots listed in `register_new_bots.py` upon startup.*

---

## 🛠 Manual Commands

If you prefer to run things outside of Docker:

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run a Single Match
```bash
python3 engine/playgame.py --map_file maps/maze/maze_p02_01.map \
  --player_names "Bot1,Bot2" \
  "python3 bots/random_bot/MyBot.py" \
  "python3 bots/statue_bot/MyBot.py"
```

### Run the Tournament Worker
```bash
python3 run_tournament.py --rounds 100
```

### Run the Web Dashboard
```bash
python3 visualizer_app.py
```

---

## 📊 Database Schema (tournament.db)

- **`players`**: Stores bot names, commands, and current ELO ratings.
- **`matches`**: Logs match timestamps and paths to replay files.
- **`match_participants`**: Links players to matches, storing their rank and score for each game.

---

## 🗺 Roadmap
- [x] Dockerization of all components.
- [x] Accurate bot naming in replays.
- [ ] Support for more programming languages in the default Docker image (C#, Rust).
- [ ] Advanced analytics (win rate per map, head-to-head stats).
- [ ] Support for "Fog of War" toggle in the visualizer.

---
© 2026 NEXTTHINGDONE. Built for the AI coding community.
