#!/usr/bin/env python
from ants import *
import random

class HeatmapBot:
    def do_turn(self, ants):
        # Very simple heatmap: Food +10, Enemy -20
        # Calculate only for tiles around my ants to save time
        
        destinations = []
        
        for a_row, a_col in ants.my_ants():
            best_dir = None
            max_score = -999999
            
            directions = list(AIM.keys())
            random.shuffle(directions)
            
            for direction in directions:
                (n_row, n_col) = ants.destination(a_row, a_col, direction)
                if not ants.passable(n_row, n_col): continue
                if (n_row, n_col) in destinations: continue
                
                # Calculate score for this tile
                score = 0
                
                # Attracted to food
                for f_row, f_col in ants.food():
                    dist = ants.distance(n_row, n_col, f_row, f_col)
                    if dist < 15:
                        score += 10 / (dist + 1)
                
                # Repelled by enemies
                for (e_row, e_col), owner in ants.enemy_ants():
                    dist = ants.distance(n_row, n_col, e_row, e_col)
                    if dist < 10:
                        score -= 20 / (dist + 1)
                
                # Attracted to enemy hills
                for (h_row, h_col), owner in ants.enemy_hills():
                    dist = ants.distance(n_row, n_col, h_row, h_col)
                    score += 50 / (dist + 1)

                if score > max_score:
                    max_score = score
                    best_dir = direction
            
            if best_dir:
                ants.issue_order((a_row, a_col, best_dir))
                destinations.append(ants.destination(a_row, a_col, best_dir))
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(HeatmapBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
