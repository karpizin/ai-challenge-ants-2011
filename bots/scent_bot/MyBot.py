#!/usr/bin/env python
from ants import *
import random

class ScentBot:
    def __init__(self):
        self.scent_map = None

    def do_turn(self, ants):
        if self.scent_map is None:
            self.scent_map = [[0 for _ in range(ants.width)] for _ in range(ants.height)]
            
        destinations = []
        
        for a_row, a_col in ants.my_ants():
            self.scent_map[a_row][a_col] += 1 # Leave scent
            
            # Look at neighbor scents
            best_dir = None
            min_scent = 999999
            
            directions = list(AIM.keys())
            random.shuffle(directions)
            
            for direction in directions:
                (n_row, n_col) = ants.destination(a_row, a_col, direction)
                if ants.passable(n_row, n_col):
                    if self.scent_map[n_row][n_col] < min_scent:
                        min_scent = self.scent_map[n_row][n_col]
                        best_dir = direction
            
            if best_dir:
                (n_row, n_col) = ants.destination(a_row, a_col, best_dir)
                if (n_row, n_col) not in destinations:
                    ants.issue_order((a_row, a_col, best_dir))
                    destinations.append((n_row, n_col))
                    continue
            
            destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(ScentBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
