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
- **Tournament Ready**: Infrastructure prepared for local Round-Robin tournaments.

## 📦 Getting Started (Docker)

The easiest way to run the challenge is via Docker, which handles all language runtimes automatically.

### 1. Build the image
```bash
docker-compose build
```

### 2. Run a sample match
```bash
docker-compose run --rm engine
```
By default, this runs a match between the built-in `RandomBot` and `HunterBot`.

### 3. Running your own bot
To test your custom bot (e.g., a Python bot):
```bash
docker-compose run --rm engine python3 engine/playgame.py \
  --map_file maps/maze/maze_p02_01.map \
  "python3 bots/my_bot/MyBot.py" \
  "python3 engine/dist/sample_bots/python/RandomBot.py"
```

## 🤖 Bot Development

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