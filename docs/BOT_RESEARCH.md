# Ants AI: Bot Research & Historical Strategies

This document summarizes the strategies of the top bots from the 2011 tournament for study and inspiration.

---

## 🔝 Top Strategies & Concepts

### 1. Influence Maps / Heatmaps
*   **Concept**: The entire map is assigned weights. Food radiates "positive" influence, while enemies radiate "negative" influence.
*   **Application**: Ants simply "roll down" the gradient towards the highest reward.
*   **Advantage**: Easily coordinates hundreds of ants without complex per-unit pathfinding.

### 2. A* Pathfinding
*   **Concept**: Using the A* algorithm to find the shortest path to food or a hill.
*   **Crucial**: Must account for the toroidal wrap ( зацикленность ) of the map.
*   **Optimization**: Pre-calculating distances between important points (all-pairs shortest paths for visible areas).

### 3. Combat Heuristics
*   **Principle**: Strength in numbers. Bots try to keep ants in clusters.
*   **Tactics**: Surrounding lone enemy ants. If an ant detects more enemies than allies within the attack radius, it retreats.

---

## 🤖 Notable Bots to Study

### goldcaddy77 (Java, Rank #143)
- **Tech**: A* Pathfinding, HeatMaps.
- **Highlights**: Ant clustering, dead-end tile detection.
- **Challenges**: Suffered from Garbage Collector pauses leading to timeouts in some games.

### ajrod (C# / Haskell)
- **Goal**: Experimenting with both Functional (Haskell) and OOP (C#) paradigms.
- **Ideas**: Used Diffusion Maps to spread ants across the map efficiently.

### xathis (Haskell, Rank #1)
- **Note**: The tournament winner. His code is the gold standard for using Influence Maps and micro-managing combat engagements.

---

## 📂 Resource Links (Offline Copy)
- `docs/specification.html` — Full game mechanics description.
- `docs/strategy_guide.html` — Official development tips.
- `engine/playgame.py` — Script for running test matches.
