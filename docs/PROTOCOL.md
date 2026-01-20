# Ants AI Game Specification

## Game Turn
1. The engine sends the map state to the bot.
2. The bot calculates moves.
3. The bot sends moves back to the engine.
4. The engine updates the game state.

## Engine Input Format
Each turn begins with lines describing the parameters (only on turn 0) and then the game state.

### Turn 0 Parameters:
- `loadtime <ms>`
- `turntime <ms>`
- `rows <int>`
- `cols <int>`
- `turns <int>`
- `viewradius2 <int>`
- `attackradius2 <int>`
- `spawnradius2 <int>`
- `ready`

### Turn N State:
- `w <row> <col>` : Water
- `f <row> <col>` : Food
- `a <row> <col> <owner>` : Ant (owner 0 is you, 1+ are enemies)
- `d <row> <col> <owner>` : Dead ant (from previous turn)
- `h <row> <col> <owner>` : Hill
- `go` : End of turn data

## Bot Output Format
- `o <row> <col> <direction>` : Orders. Direction is one of 'N', 'E', 'S', 'W'.
- `go` : Finish orders for the turn.

## Combat Logic
Combat is 1:1 ratio based on radial distance. If an ant is in range of more enemies than allies (within `attackradius2`), it dies.
Actual implementation is more complex (focused on resolving group battles simultaneously).
