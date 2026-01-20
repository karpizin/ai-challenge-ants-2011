#!/usr/bin/env python
from ants import *

class GreedyFoodBot:
    def do_turn(self, ants):
        destinations = []
        food_targets = set()
        
        for a_row, a_col in ants.my_ants():
            closest_food = ants.closest_food(a_row, a_col, filter=food_targets)
            if closest_food:
                directions = ants.direction(a_row, a_col, closest_food[0], closest_food[1])
                moved = False
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if (not (n_row, n_col) in destinations and
                            ants.passable(n_row, n_col)):
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        food_targets.add(closest_food)
                        moved = True
                        break
                if not moved:
                    destinations.append((a_row, a_col))
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(GreedyFoodBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
