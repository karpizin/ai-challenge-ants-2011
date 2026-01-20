#!/usr/bin/env python
from ants import *
import random

class ExplorerBot:
    def do_turn(self, ants):
        destinations = []
        
        for a_row, a_col in ants.my_ants():
            # Quick check for nearby unseen
            best_dir = None
            found_unseen = False
            
            directions = list(AIM.keys())
            random.shuffle(directions)
            
            # Simple heuristic: move to a direction that has more UNSEEN tiles in its general direction
            # Or just pick the first direction that leads to an UNSEEN tile or closer to one
            
            # Fallback to a simpler exploration if closest_unseen is too slow
            # For now, let's just use random walk if we don't want to scan the whole map
            # but let's try to find an UNSEEN tile in a small radius first
            
            for direction in directions:
                (n_row, n_col) = ants.destination(a_row, a_col, direction)
                if ants.passable(n_row, n_col) and (n_row, n_col) not in destinations:
                    if ants.map[n_row][n_col] == UNSEEN:
                        best_dir = direction
                        found_unseen = True
                        break
            
            if not found_unseen:
                # Try to move towards some distant unseen (very simplified)
                # To keep it "Simple", we'll just do a random valid move if no immediate unseen
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col, direction)
                    if ants.passable(n_row, n_col) and (n_row, n_col) not in destinations:
                        best_dir = direction
                        break
            
            if best_dir:
                ants.issue_order((a_row, a_col, best_dir))
                destinations.append(ants.destination(a_row, a_col, best_dir))
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(ExplorerBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
