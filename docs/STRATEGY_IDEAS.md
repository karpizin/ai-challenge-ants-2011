# 20 AI Bot Ideas (Ants AI Challenge)

This list contains bot concepts of varying complexity—from "educational" baselines to competitive heuristics.

---

### 1. Level: "Starter" (Basics)
1.  **RandomBot**: Selects a random direction (N, S, E, W) for each ant.
2.  **StatueBot**: Ants never move. Used to test enemy attack logic.
3.  **LeftyBot**: Always tries to turn left (walking in circles/along walls).
4.  **GreedyFoodBot**: Finds the closest food in visible range and moves directly towards it. Stays still if no food is visible.
5.  **ExplorerBot**: Moves towards the closest tile that hasn't been revealed yet (Fog of War exploration).

---

### 2. Level: "Am Amateur" (Simple Heuristics)
6.  **DistanceBot**: Uses BFS (Breadth-First Search) to find the shortest path to food, ignoring obstacles until it hits them.
7.  **SafetyFirstBot**: Moves towards food but retreats in the opposite direction if an enemy is detected within `attackradius`.
8.  **AggressiveHillBot**: Ignores food and searches for enemy hills. Once found, all ants swarm the target.
9.  **ScentBot (Pheromones)**: Each tile an ant visits gains a "scent". Other ants avoid "fresh" tracks to distribute themselves across the map.
10. **ZonalBot**: Divides the map into sectors. Each ant is assigned to a specific zone and patrols only that area.

---

### 3. Level: "Intermediate" (Influence Maps)
11. **SimpleHeatmapBot**: Food gives +10 to a tile, enemies give -50. Ants move to the adjacent tile with the highest weight.
12. **DiffusionBot**: Implements simple weight diffusion (like heat dissipation) to fill "voids" on the map with information.
13. **AntCapBot**: Limits the number of ants heading to the same piece of food (e.g., no more than 2 ants per crumb).
14. **HillDefenderBot**: 20% of the population always remains within a 5-tile radius of the home hill.
15. **SuicideSquadBot**: If an ant sees a hill, it charges it at any cost, regardless of surrounding enemies.

---

### 4. Level: "Advanced" (Tactical)
16. **CombatMicroBot**: Simulates the combat outcome before moving. If the outcome is death, it picks a different move.
17. **DeadEndAvoider**: Pre-scans the map to identify and mark dead-ends. Ants only enter dead-ends if food is present.
18. **SupportBot**: Ants try to move in pairs. A lone ant waits for a teammate before engaging in combat.
19. **FoodChainBot**: Builds a chain of ants from food to the hill for fast "hand-off" (efficient on narrow corridor maps).
20. **TimeManagerBot**: Adjusts calculation depth based on remaining `turntime` (250ms). Switches to Random logic if time is low.

---

## 🛠 How to Use These Ideas
Each idea can be implemented as a standalone `MyBot.py` or `MyBot.java` file. 
Running a tournament between **RandomBot** and **SimpleHeatmapBot** is a great way to verify how much more effective influence maps are compared to random walks.