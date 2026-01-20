#!/usr/bin/env python
from ants import *
from collections import deque

class DistanceBot:
    def bfs_path(self, ants, start, targets):
        if not targets: return None
        queue = deque([start])
        visited = {start: None}
        target_set = set(targets)
        
        while queue:
            curr = queue.popleft()
            if curr in target_set:
                # Reconstruct path
                while visited[curr] != start:
                    curr = visited[curr]
                return curr
                
            for direction in AIM.keys():
                next_loc = ants.destination(curr[0], curr[1], direction)
                if next_loc not in visited and ants.passable(next_loc[0], next_loc[1]):
                    visited[next_loc] = curr
                    queue.append(next_loc)
        return None

    def do_turn(self, ants):
        destinations = []
        food_targets = set(ants.food())
        
        for a_row, a_col in ants.my_ants():
            next_step = self.bfs_path(ants, (a_row, a_col), food_targets)
            if next_step:
                # find which direction leads to next_step
                for direction in AIM.keys():
                    if ants.destination(a_row, a_col, direction) == next_step:
                        if next_step not in destinations:
                            ants.issue_order((a_row, a_col, direction))
                            destinations.append(next_step)
                            break
                else:
                    destinations.append((a_row, a_col))
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        Ants.run(DistanceBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
