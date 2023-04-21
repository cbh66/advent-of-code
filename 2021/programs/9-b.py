#!/usr/bin/python3

import sys
from pprint import pprint

def neighbors(min, i, max):
    if min <= i - 1:
        yield i - 1
    if i + 1 <= max:
        yield i + 1

def basin_size(inputs, coords):
    points_to_check = [coords]
    basin_points = set()
    max_row = len(inputs) - 1
    max_col = len(inputs[max_row]) - 1
    while len(points_to_check) > 0:
        (row, col) = points_to_check.pop()
        basin_points.add((row, col))
        for n_r in neighbors(0, row, max_row):
            if (n_r, col) not in basin_points and int(inputs[n_r][col]) != 9:
                points_to_check.append((n_r, col))
        for n_c in neighbors(0, col, max_col):
            if (row, n_c) not in basin_points and int(inputs[row][n_c]) != 9:
                points_to_check.append((row, n_c))
    # print(basin_points)
    return len(basin_points)


def main(inputs):
    min_points = []
    max_row = len(inputs) - 1
    for row_num in range(len(inputs)):
        row = inputs[row_num]
        max_col = len(row) - 1
        for col_num in range(len(row)):
            lower_neighbors = 0
            for n_r in neighbors(0, row_num, max_row):
                if int(inputs[n_r][col_num]) <= int(inputs[row_num][col_num]):
                    lower_neighbors += 1
            for n_c in neighbors(0, col_num, max_col):
                if int(inputs[row_num][n_c]) <= int(inputs[row_num][col_num]):
                    lower_neighbors += 1
            if lower_neighbors == 0:
                min_points.append((row_num, col_num))

    # loop thru min points
    # get basin size for each
    sizes = sorted([basin_size(inputs, point) for point in min_points], reverse=True)
    print(f'{sizes[0]} * {sizes[1]} * {sizes[2]} = {sizes[0] * sizes[1] * sizes[2]}')


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
