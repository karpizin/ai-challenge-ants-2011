#!/usr/bin/env python
from ants import *
import random

class AggressiveHillBot:
    def do_turn(self, ants):
        destinations = []
        
        # Priority 1: Hills
        # Priority 2: Food (if no hill seen)
        
        for a_row, a_col in ants.my_ants():
            target = ants.closest_enemy_hill(a_row, a_col)
            if not target:
                target = ants.closest_food(a_row, a_col)
                
            if target:
                directions = ants.direction(a_row, a_col, target[0], target[1])
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
                # Explore randomly
                directions = list(AIM.keys())
                random.shuffle(directions)
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if (not (n_row, n_col) in destinations and ants.passable(n_row, n_col)):
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        break
                else:
                    destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(AggressiveHillBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
