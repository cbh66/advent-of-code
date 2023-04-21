#!/usr/bin/python3

import sys
import re
from pprint import pprint

SEGMENT_REGEX = re.compile(r'(\w+)\-(\w+)')

class Cave:
    def __init__(self, name):
        self.name = name
        self.num_visits = 0
        self.neighbors = set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor.name)

    def can_enter(self):
        name = self.name
        num_visits = self.num_visits
        return name != 'start' and (name.isupper() or num_visits < 1)

    def __repr__(self):
        return f'{self.name} {self.neighbors}'


# returns list of paths from start to end, not visiting lowercase names more than once
# each path is a list of strings starting with start and ending with end
def paths(caves, start: str, end: str, can_double_visit=True):
    if start == end:
        return [(end,)]
    if start not in caves:
        return []

    if start.islower():
        caves_copy = caves.copy()
        del caves_copy[start]
    else:
        caves_copy = caves
    caves[start].num_visits += 1

    all_paths = set()
    for neighbor_name in caves[start].neighbors:
        all_paths.update(paths(caves_copy, neighbor_name, end, can_double_visit=can_double_visit))
    if start != 'start' and start.islower() and can_double_visit:
        for neighbor_name in caves[start].neighbors:
            all_paths.update(paths(caves, neighbor_name, end, can_double_visit=False))
    
    all_paths = [(start,) + (p) for p in all_paths]
    caves[start].num_visits -= 1
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
    all_paths = paths(caves, 'start', 'end')
    # print(len(paths(caves, 'start', 'end')))
    # pprint(sorted([','.join(p) for p in all_paths]))
    print(len(all_paths))
    # pprint(caves)
    pass

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
