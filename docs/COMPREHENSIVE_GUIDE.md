# Ants AI Challenge: The Comprehensive Guide

This document provides a detailed technical reference for the Ants AI Challenge 2011 restoration project. It is intended for developers building bots or maintaining the tournament infrastructure.

---

## 1. Game Mechanics Deep Dive

### 1.1 The Map
- **Grid**: The game is played on a rectangular grid of `rows` by `cols`.
- **Topology**: The map is a **torus**. Moving off the North edge places you on the South edge at the same column. Moving East wraps to the West.
- **Tile Types**:
  - `Land`: Open ground where ants can move.
  - `Water`: Impassable obstacles.
  - `Food`: Neutral objects that spawn new ants when collected.
  - `Ant`: Occupied by a player's ant.
  - `Hill`: A player's base. If an enemy occupies this tile, the hill is destroyed.

### 1.2 Movement
- Ants can move in four cardinal directions: **North (N), East (E), South (S), West (W)**.
- Only one ant can occupy a tile at the end of a turn.
- If two ants of the same player move to the same tile, one is destroyed (collision).
- If ants from different players move to the same tile, combat logic is triggered.

### 1.3 Food & Spawning
- When an ant moves onto a `Food` tile, it is "collected."
- Collected food is converted into a new ant at the player's closest `Hill`.
- If a player has no hills, they cannot spawn new ants.

### 1.4 Combat Logic (The 1:1 Rule)
The engine resolves combat using a radial system:
1. For every ant, count enemy ants within `attackradius2`.
2. For every ant, count allied ants (including itself) within `attackradius2`.
3. If an ant has **more or equal** enemies in range than allies, it is marked for death.
4. All marked ants are removed simultaneously.

---

## 2. Technical Protocol (stdin/stdout)

Your bot must read from `stdin` and write to `stdout`.

### 2.1 Initialization (Turn 0)
The engine sends game parameters followed by `ready`. You have `loadtime` (e.g., 3000ms) to initialize.
```text
loadtime 3000
turntime 500
rows 100
cols 100
turns 500
viewradius2 77
attackradius2 5
spawnradius2 1
ready
```

### 2.2 Turn Cycle
Every turn, the engine sends the visible map data:
- `w <row> <col>` : Water discovered.
- `f <row> <col>` : Food visible.
- `a <row> <col> <owner>` : Ant visible (owner 0 is you).
- `d <row> <col> <owner>` : Dead ant from last turn.
- `h <row> <col> <owner>` : Hill visible.
- `go` : Start calculating.

### 2.3 Issuing Orders
Send orders in the format: `o <row> <col> <direction>`. End your turn with `go`.
```text
o 12 45 N
o 15 20 E
go
```

---

## 3. Toroidal Mathematics

When calculating distances, you must use the shortest path across the wrap-around edges.

**Distance between (r1, c1) and (r2, c2):**
```python
def get_distance(r1, c1, r2, c2, rows, cols):
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    # Wrap around if the direct path is longer than half the map
    row_dist = min(dr, rows - dr)
    col_dist = min(dc, cols - dc)
    return row_dist + col_dist # Manhattan distance
```

---

## 4. Advanced Strategic Patterns

### 4.1 Influence Maps (Heatmaps)
Instead of pathfinding for every single ant, maintain a 2D array of floats representing "desirability."
1. Start with a zeroed map.
2. For every Food tile, add `+1.0` and diffuse it to neighbors (e.g., `val * 0.9`).
3. For every enemy Hill, add `+10.0`.
4. For every enemy Ant, subtract `-2.0` (danger zone).
5. Ants move to the adjacent tile with the highest value.

### 4.2 Diffusion
Use a simple blur algorithm to spread "scent" across the map:
`Map[turn+1][x][y] = (Map[turn][x][y] + neighbors_sum) / 5`

---

## 5. Development & Docker Workflow

### 5.1 Compilation
If using a compiled language (C++, Go, Rust, Java), you must compile inside the container:
```bash
docker-compose run --rm engine bash -c "cd bots/my_bot && make"
```

### 5.2 Local Visualization
The engine produces a `.replay` file or a replay string. To view a match in real-time or from a file:
1. Replays are saved in the `replays/` directory.
2. Use the `engine/visualizer/visualize_locally.py` script to host a local viewer.

---

## 6. Official Rules & Constraints
- **Time Limit**: Usually 250ms - 500ms per turn. Exceeding this results in a timeout and loss.
- **Memory**: Max 512MB RAM typically.
- **Threading**: Standard computational logic must be single-threaded.
- **File Access**: Bots cannot save data between games.
