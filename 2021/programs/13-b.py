#!/usr/bin/python3

import sys
import re
from pprint import pprint

FOLD_REGEX = re.compile(r'fold along ((x|y)=([0-9]+))')

def folded_destination(i, fold_line):
    return (2 * fold_line) - i

def fold_row(row, fold):
    new_row = [x for x in row[:fold]]
    for i in range(fold + 1, len(row)):
        folded_index = folded_destination(i, fold)
        new_row[folded_index] = new_row[folded_index] or row[i]
    return new_row

def merge_rows(row1, row2):
    return [row1[i] or row2[i] for i in range(min(len(row1), len(row2)))]

class Paper:
    def __init__(self, dot_list):
        width = max([x for (x, _) in dot_list]) + 1
        height = max(y for (_, y) in dot_list) + 1
        self.grid = [[False] * width for _ in range(height)]
        for (x, y) in dot_list:
            self.grid[y][x] = True

    def __repr__(self):
        return '\n'.join([
            ''.join(['#' if square else '.' for square in row])
            for row in self.grid
        ])

    def fold_along_vertical(self, y):
        self.grid = [
            fold_row(row, y)
            for row in self.grid
        ]

    def fold_along_horizontal(self, x):
        new_grid = self.grid[:x]
        for i in range(x + 1, len(self.grid)):
            folded_index = folded_destination(i, x)
            new_grid[folded_index] = merge_rows(new_grid[folded_index], self.grid[i])
        self.grid = new_grid

    def num_dots(self):
        return sum([sum([1 if s else 0 for s in row]) for row in self.grid])


def main(inputs):
    dots = []  # x,y tuples
    folds = [] # 'x'|'y', int tuples
    for line in inputs:
        if not line: continue
        match = FOLD_REGEX.match(line)
        if match:
            print(match.groups())
            folds.append((match.group(2), int(match.group(3))))
        else:
            coords = line.split(',')
            dots.append((int(coords[0]), int(coords[1])))
    
    paper = Paper(dots)
    for (direction, index) in folds:
        if direction == 'y':
            paper.fold_along_horizontal(index)
        elif direction == 'x':
            paper.fold_along_vertical(index)
        print(paper)
        # print(paper.num_dots())
        # break

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
