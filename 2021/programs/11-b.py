#!/usr/bin/python3

import sys
from pprint import pprint

class Octopus:
    def __init__(self, power):
        self.neighbors = set()
        self.power = power
        self.has_flashed = False

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def set_power(self, power):
        self.power = power

    def next_step(self):
        self.power += 1
        if self.power > 9 and not self.has_flashed:
            self.has_flashed = True
            for neighbor in self.neighbors:
                neighbor.next_step()

    def end_step(self):
        self.has_flashed = False
        if self.power > 9:
            self.power = 0

    def __repr__(self):
        return str(self.power)

def neighbors(grid, row, col):
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    for r in range(max(0, row - 1), min(row + 1, max_row) + 1):
        for c in range(max(0, col - 1), min(col + 1, max_col) + 1):
            if r != row or c != col:
                yield (r, c)

# returns true if every octopus flashed, else false
def step(grid):
    for row in grid:
        for octopus in row:
            octopus.next_step()
    all_flashed = True
    for row in grid:
        for octopus in row:
            if not octopus.has_flashed:
                all_flashed = False
            octopus.end_step()
    return all_flashed

def main(inputs):
    grid = [
        [Octopus(int(c)) for c in input]
        for input in inputs
    ]
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            for (r, c) in neighbors(grid, row, col):
                grid[row][col].add_neighbor(grid[r][c])
    i = 0
    while not step(grid):
        i += 1
    pprint(grid)
    print(i + 1)
    


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
