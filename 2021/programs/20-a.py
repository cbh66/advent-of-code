#!/usr/bin/python3

import sys

# can start w 2d array, but if efficiency matters later, maybe just hash coords
# or the hash may be easier to handle negative nums and resizing, and can just
# put into a grid for printing

class InfiniteGrid:
    def __init__(self, default_val):
        self.default_val = default_val
        self._rows = {}

    def get(self, coords):
        (x, y) = coords
        if y not in self._rows or x not in self._rows[y]:
            return self.default_val
        return self._rows[y][x]
        
    def set(self, coords, value):
        if value == self.default_val:
            return
        (x, y) = coords
        if y not in self._rows:
            self._rows[y] = {}
        self._rows[y][x] = value

    def non_default_keys(self):
        return [
            (x, y)
            for y in self._rows
            for x in self._rows[y]
        ]

def to_image(grid):
    keys = grid.non_default_keys()
    x_start = min(x for (x, _) in keys)
    x_end = max(x for (x, _) in keys)
    y_start = min(y for (_, y) in keys)
    y_end = max(y for (_, y) in keys)
    return '\n'.join([
        ''.join([
            grid.get((x, y))
            for x in range(x_start - 2, x_end + 3)
        ])
        for y in range(y_start - 2, y_end + 3)
    ])
        
def neighbors(coord):
    (x_center, y_center) = coord
    for x in range(x_center - 1, x_center + 2):
        for y in range(y_center - 1, y_center + 2):
            yield (x, y)

def calculate_alg_index(coord, grid):
    index = 0
    place = 2 ** 8
    (x_center, y_center) = coord
    for y in range(y_center - 1, y_center + 2):
        for x in range(x_center - 1, x_center + 2):
            if grid.get((x, y)) != '.':
                index += place
            place = place // 2
    return index

def all_neighborly_points(grid):
    points = set()
    for (x_center, y_center) in grid.non_default_keys():
        for y in range(y_center - 1, y_center + 2):
            for x in range(x_center - 1, x_center + 2):
                points.add((x, y))
    return points

def iterate(grid, algorithm):
    points = all_neighborly_points(grid)
    arbitrary_edge_point = (min(x for (x, _) in points), min(y for (_, y) in points))
    default_index = calculate_alg_index(arbitrary_edge_point, grid)
    new_grid = InfiniteGrid(default_val=algorithm[default_index])
    for coord in all_neighborly_points(grid):
        index = calculate_alg_index(coord, grid)
        new_grid.set(coord, algorithm[index])
    return new_grid

def main(inputs):
    alg = ''
    i = 0
    while len(inputs[i]) > 0:
        alg += inputs[i]
        i += 1

    image = inputs[i + 1:]
    grid = InfiniteGrid(default_val='.')
    for y in range(len(image)):
        for x in range(len(image[y])):
            grid.set((x, y), image[y][x])

    for _ in range(2):
        grid = iterate(grid, alg)
        # print(to_image(grid))
    print(len(grid.non_default_keys()))


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
