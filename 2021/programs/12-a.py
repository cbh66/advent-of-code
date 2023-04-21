#!/usr/bin/python3

import sys
import re
from pprint import pprint

SEGMENT_REGEX = re.compile(r'(\w+)\-(\w+)')

class Cave:
    def __init__(self, name):
        self.name = name
        self.is_visited = False
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor.name)

    def can_visit(self):
        return self.name.isupper() or not self.is_visited

    def visit(self):
        self.is_visited = True

    def reset(self):
        self.is_visited = False

    def __repr__(self):
        return f'{self.name} {self.neighbors}'


# returns list of paths from start to end, not visiting lowercase names more than once
# each path is a list of strings starting with start and ending with end
def paths(caves, start: str, end: str):
    if start == end:
        return [[end]]
    if start not in caves:
        return []

    if start.islower():
        # can't visit again
        caves_copy = caves.copy()
        del caves_copy[start]
    else:
        caves_copy = caves

    all_paths = []
    for neighbor_name in caves[start].neighbors:
        all_paths.extend(paths(caves_copy, neighbor_name, end))
    for path in all_paths:
        path.insert(0, start)
    return all_paths


def add_connection(caves, cave_name_1, cave_name_2):
    if cave_name_1 not in caves:
        caves[cave_name_1] = Cave(cave_name_1)
    if cave_name_2 not in caves:
        caves[cave_name_2] = Cave(cave_name_2)
    caves[cave_name_1].add_neighbor(caves[cave_name_2])
    caves[cave_name_2].add_neighbor(caves[cave_name_1])

def main(inputs):
    caves = {
        'start': Cave('start'),
        'end': Cave('end'),
    }
    for input in inputs:
        match = SEGMENT_REGEX.match(input)
        if match is None:
            print('bad match')
        add_connection(caves, match.group(1), match.group(2))
    print(len(paths(caves, 'start', 'end')))
    # pprint(caves)
    pass

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
