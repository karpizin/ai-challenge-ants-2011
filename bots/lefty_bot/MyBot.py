#!/usr/bin/env python
from ants import *

class LeftyBot:
    def __init__(self):
        self.ant_directions = {} # track direction for each ant

    def do_turn(self, ants):
        destinations = []
        new_ant_directions = {}
        
        for a_row, a_col in ants.my_ants():
            # Get last direction or start with 'n'
            last_dir = self.ant_directions.get((a_row, a_col), 'n')
            
            # Try to turn left, then straight, then right, then back
            directions = [LEFT[last_dir], last_dir, RIGHT[last_dir], BEHIND[last_dir]]
            
            moved = False
            for direction in directions:
                (n_row, n_col) = ants.destination(a_row, a_col, direction)
                if (not (n_row, n_col) in destinations and
                        ants.passable(n_row, n_col)):
                    ants.issue_order((a_row, a_col, direction))
                    destinations.append((n_row, n_col))
                    new_ant_directions[(n_row, n_col)] = direction
                    moved = True
                    break
            
            if not moved:
                destinations.append((a_row, a_col))
                new_ant_directions[(a_row, a_col)] = last_dir
                
        self.ant_directions = new_ant_directions

if __name__ == '__main__':
    try:
        Ants.run(LeftyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
