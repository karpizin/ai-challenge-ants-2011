# Ants AI Challenge 2011 (Restoration Project) 🐜

A robust restoration of the legendary **Google AI Challenge 2011 (Ants)**. This project provides a complete local environment for developing, testing, and ranking AI bots across multiple programming languages.

## 🕹 Game Overview
You control a colony of ants on a 2D grid (usually a toroidal map).
- **Objectives**: Collect food to spawn more ants, defend your hills, and destroy enemy hills.
- **Fog of War**: You can only see within a specific radius of your ants.
- **Toroidal Topology**: Maps often wrap around edges (North to South, East to West).

## 🚀 Features
- **Original Engine**: The official Python-based game engine (`playgame.py`).
- **Dockerized Environment**: Pre-configured support for **Python, Java, C++, Node.js, Go, and Rust**.
- **Massive Map Library**: Over 1,000 official maps included.
- **Multi-language Starters**: Ready-to-use starter packages for 25+ languages.
- **Tournament Manager**: Automated Round-Robin tournament system with SQLite backend and ELO ratings.
- **Web Visualizer**: FastAPI-based dashboard to view leaderboard and watch match replays.

## 📦 Getting Started (Local)

### 1. Run a Tournament
Register the baseline bots and start 10 rounds of matches:
```bash
python3 register_new_bots.py
python3 run_tournament.py --rounds 10
```

### 2. View Leaderboard & Replays
Start the web server:
```bash
python3 visualizer_app.py
```
Open `http://localhost:8000` in your browser.

## 🤖 Bot Development

### Baseline Bots
We have included 10 implementation examples in the `bots/` directory:
- `random_bot`, `statue_bot`, `lefty_bot`, `greedy_food_bot`, `explorer_bot`
- `distance_bot` (BFS), `safety_first_bot`, `aggressive_hill_bot`, `scent_bot`, `heatmap_bot`

### The Protocol
Communication happens via `stdin` and `stdout`. Each turn, the engine sends the current visible state, and the bot must respond with commands (`o <row> <col> <dir>`) followed by `go`.

Detailed specs can be found in [docs/PROTOCOL.md](docs/PROTOCOL.md).

### Strategy Ideas
Check out [docs/STRATEGY_IDEAS.md](docs/STRATEGY_IDEAS.md) for 20 algorithmic concepts to implement, ranging from simple greedy search to complex influence maps.

## 🏗 Project Structure
- `engine/`: The core Python game engine and original tools.
- `bots/`: Place your custom bot implementations here.
- `maps/`: A vast collection of .map files for training and testing.
- `docs/`: Technical specifications and strategy guides.
- `tools/`: Utility scripts for tournament management and visualization.

## 🛠 Tech Stack
- **Engine**: Python 3.11
- **Runtimes**: OpenJDK 17, GCC, Node.js, Go, Rust (rustup)
- **Containerization**: Docker & Docker Compose

---
*This project is a tribute to the original AI Challenge community. All assets are maintained for educational and historical purposes.*