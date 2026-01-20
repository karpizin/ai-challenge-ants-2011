#!/usr/bin/env python
from ants import *

class StatueBot:
    def do_turn(self, ants):
        # I just stand here and look pretty.
        pass

if __name__ == '__main__':
    try:
        Ants.run(StatueBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
