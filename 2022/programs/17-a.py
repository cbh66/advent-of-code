#!/usr/bin/python3

import sys

ROCKS = [
'''####''',
'''
 # 
###
 # 
''',
'''
###
  #
  #
''',
'''
#
#
#
#
''',
'''
##
##
'''
]
class WrappingList:
    def __init__(self, values):
        self.i = 0
        self._values = values

    def next(self):
        v = self._values[self.i]
        self.i = (self.i + 1) % len(self._values)
        return v

class Chamber:
    def __init__(self, jets):
        self._grid = [[c for c in '#' * 9]]
        self._jets = WrappingList(jets)
        self._rocks = WrappingList([
            [
                [c for c in line]
                for line in rock.split('\n') if line.strip()
            ]
            for rock in ROCKS
        ])

    def drop_next_rock(self):
        rock = self._rocks.next()
        self._ensure_room((len(rock) + 3))
        rock_row = self.highest_rock_row() + 4
        rock_col = 3
        while True:
            command = self._jets.next()
            dir = -1 if command == '<' else 1
            if self._can_move(rock, (rock_row, rock_col), (0, dir)):
                rock_col += dir
            if self._can_move(rock, (rock_row, rock_col), (-1, 0)):
                rock_row -= 1
            else:
                break
        for r in range(len(rock)):
            grid_row = rock_row + r
            for c in range(len(rock[r])):
                grid_col = rock_col + c
                if rock[r][c] == '#':
                    self._grid[grid_row][grid_col] = '#'

    def _ensure_room(self, rows):
        top_row = self.highest_rock_row()
        self._grid += [[c for c in '#       #'] for i in range(rows - (len(self._grid) - top_row - 1))]

    def highest_rock_row(self):
        for row in reversed(range(len(self._grid))):
            if any('#' in col for col in self._grid[row][1:-1]):
                return row
        return None

    def _can_move(self, rock, coords, direction):
        (rock_row, rock_col) = coords
        (d_row, d_col) = direction
        for r in range(len(rock)):
            grid_row = rock_row + r
            for c in range(len(rock[r])):
                grid_col = rock_col + c
                if rock[r][c] == '#':
                    if self._grid[grid_row + d_row][grid_col + d_col] == '#':
                        return False
        return True

    def print(self):
        for row in reversed(self._grid):
            print(''.join(row))

def main(input):
    chamber = Chamber(input.strip())
    for i in range(2022):
        chamber.drop_next_rock()
    print(chamber.highest_rock_row())

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()][0])
