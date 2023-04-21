#!/usr/bin/python3

import sys
import re
from pprint import pprint

# just processes the offsets output for part 1

def man_dist(c1, c2):
    return sum([abs(c1[dim] - c2[dim]) for dim in range(3)])

def largest_man_dist(coords):
    return max([
        man_dist(c1, c2)
        for c1 in coords
        for c2 in coords
    ])
    
def main(inputs):
    offsets = [[int(x) for x in input.split(',')] for input in inputs]
    print(f'Max distance between scanners: {largest_man_dist(offsets)}')

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
