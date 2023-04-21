#!/usr/bin/python3

import sys
import math

def nice_grid(grid):
    return '\n'.join([''.join(row) for row in grid])

# returns [new grid, num movements made]
def step(grid):
    num_movements = 0
    new_grid = [['.' for _ in row] for row in grid]
    # first step east
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '>':
                next_col = (col + 1) % len(grid[row])
                destination_col = col
                if grid[row][next_col] == '.':
                    num_movements += 1
                    destination_col = next_col
                new_grid[row][destination_col] = '>'
            elif grid[row][col] == 'v':
                new_grid[row][col] = 'v'

    grid = new_grid
    new_grid = [['.' for _ in row] for row in grid]

    # then step south
    for row in range(len(grid)):
        next_row = (row + 1) % len(grid)
        for col in range(len(grid[row])):
            if grid[row][col] == 'v':
                destination_row = row
                if grid[next_row][col] == '.':
                    num_movements += 1
                    destination_row = next_row
                new_grid[destination_row][col] = 'v'
            elif grid[row][col] == '>':
                new_grid[row][col] = '>'
    return [new_grid, num_movements]


def main(inputs):
    grid = [row for row in inputs]
    i = 0
    num_movements = math.inf
    while num_movements > 0:
        # print(f'Step {i}')
        # print(nice_grid(grid))
        [grid, num_movements] = step(grid)
        i += 1
    # print()
    # print(nice_grid(grid))
    print(f'{i} steps')


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
