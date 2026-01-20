#!/usr/bin/env python
from ants import *
import random

class SafetyFirstBot:
    def do_turn(self, ants):
        destinations = []
        
        for a_row, a_col in ants.my_ants():
            # Check for nearby enemies
            closest_enemy = ants.closest_enemy_ant(a_row, a_col)
            if closest_enemy and ants.distance(a_row, a_col, closest_enemy[0], closest_enemy[1]) < 5:
                # RETREAT! Find direction away from enemy
                enemy_dirs = ants.direction(a_row, a_col, closest_enemy[0], closest_enemy[1])
                safe_dirs = [d for d in AIM.keys() if d not in enemy_dirs]
                random.shuffle(safe_dirs)
                
                moved = False
                for direction in safe_dirs:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if (not (n_row, n_col) in destinations and ants.passable(n_row, n_col)):
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        moved = True
                        break
                if not moved: destinations.append((a_row, a_col))
                continue

            # If safe, go for food
            closest_food = ants.closest_food(a_row, a_col)
            if closest_food:
                directions = ants.direction(a_row, a_col, closest_food[0], closest_food[1])
                random.shuffle(directions)
                moved = False
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if (not (n_row, n_col) in destinations and ants.passable(n_row, n_col)):
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        moved = True
                        break
                if not moved: destinations.append((a_row, a_col))
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(SafetyFirstBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
