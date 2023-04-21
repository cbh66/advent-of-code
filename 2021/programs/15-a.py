#!/usr/bin/python3

import sys
from pprint import pprint

class Square:
    def __init__(self, risk):
        self.risk = risk
        self.best_known_path_score = None

    def __repr__(self):
        return str(self.best_known_path_score)

def build_basic_paths(grid):
    grid[0][0].best_known_path_score = 0
    # go thru first row and add score to one on left
    for x in range(1, len(grid[0])):
        grid[0][x].best_known_path_score = grid[0][x].risk + grid[0][x-1].best_known_path_score
    # go thru first col and add score to one above
    for y in range(1, len(grid)):
        grid[y][0].best_known_path_score = grid[y][0].risk + grid[y-1][0].best_known_path_score

    # pprint(grid)
    for y in range(1, len(grid)):
        for x in range(1, len(grid[y])):
            neighbor_scores = [
                grid[y-1][x].best_known_path_score,
                grid[y][x-1].best_known_path_score
            ]
            # print(f'{y}, {x}')
            # pprint(neighbor_scores)
            # pprint(grid)
            grid[y][x].best_known_path_score = grid[y][x].risk + min(neighbor_scores) 

def main(inputs):
    grid = [
        [Square(int(c)) for c in row]
        for row in inputs
    ]
    build_basic_paths(grid)
    print(grid[-1][-1].best_known_path_score)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
