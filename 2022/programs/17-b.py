#!/usr/bin/python3
import sys
from collections import deque

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
        self._amt_shaved = 0

    def drop_next_rock(self):
        rock = self._rocks.next()
        self._ensure_room((len(rock) + 3))
        rock_row = self.highest_rock_row() - self._amt_shaved + 4
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
        top_row = self.highest_rock_row() - self._amt_shaved
        self._grid += [[c for c in '#       #'] for i in range(rows - (len(self._grid) - top_row - 1))]
        if (len(self._grid) > 2500):
            self._amt_shaved += len(self._grid) - 1000
            self._grid = self._grid[-1000:]

    def highest_rock_row(self):
        for row in reversed(range(len(self._grid))):
            if any('#' in col for col in self._grid[row][1:-1]):
                return row + self._amt_shaved
        return None

    def top(self, num_rows):
        return [''.join(row) for row in self._grid[len(self._grid) - num_rows - 1 : len(self._grid) - 1]]

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

def is_same_grid(g1, g2):
    for row in range(min(len(g1), len(g2))):
        if g1[row] != g2[row]:
            return False
    return True

def find_period(input):
    chamber = Chamber(input)
    for i in range(40000):
        chamber.drop_next_rock()
    last_several_moves = deque()
    for i in range(40000, 50000):
        chamber.drop_next_rock()
        last_several_moves.append({
            'move': i,
            'height': chamber.highest_rock_row(),
            'top': chamber.top(50),
        })
    for i in range(50000, 1_000_000_000_000):
        chamber.drop_next_rock()
        top = chamber.top(50)
        for prev_move_i in reversed(range(len(last_several_moves))):
            prev_move = last_several_moves[prev_move_i]
            if is_same_grid(top, prev_move['top']):
                return {
                    'ref_move': i - 1,
                    'ref_height': last_several_moves[-1]['height'],
                    'pattern': [
                        last_several_moves[x]['height'] - last_several_moves[prev_move_i - 1]['height']
                        for x in range(prev_move_i, len(last_several_moves))
                    ],
                }
        last_several_moves.popleft()
        last_several_moves.append({
            'move': i,
            'height': chamber.highest_rock_row(),
            'top': top,
        })

def main(input):
    result = find_period(input.strip())
    i = result['ref_move']
    height = result['ref_height']
    pattern = result['pattern']
    NUM_ITERATIONS = 1_000_000_000_000
    height += pattern[-1] * ((NUM_ITERATIONS - i) // len(pattern))
    i = (NUM_ITERATIONS - i - 1) % len(pattern)
    height += pattern[(i - 1) % len(pattern)]
    print(height)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()][0])
