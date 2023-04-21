#!/usr/bin/python3

import sys
import re

STEP_REGEX = re.compile(r'(on|off) x=(\S+)\.\.(\S+),y=(\S+)\.\.(\S+),z=(\S+)\.\.(\S+)')

class InfiniteSpace:
    def __init__(self, default_val):
        self.default_val = default_val
        self._planes = {}

    def get(self, coords):
        (x, y, z) = coords
        if z not in self._planes or y not in self._planes[z] or x not in self._planes[z][y]:
            return self.default_val
        return self._planes[z][y][x]
        
    def set(self, coords, value):
        (x, y, z) = coords
        if z not in self._planes:
            self._planes[z] = {}
        if y not in self._planes[z]:
            self._planes[z][y] = {}
        self._planes[z][y][x] = value

    def non_default_keys(self):
        return [
            (x, y, z)
            for z in self._planes
            for y in self._planes[z]
            for x in self._planes[z][y]
        ]

def main(inputs):
    space = InfiniteSpace(False)
    for input in inputs:
        match = STEP_REGEX.match(input)
        min_x = int(match.group(2))
        max_x = int(match.group(3))
        min_y = int(match.group(4))
        max_y = int(match.group(5))
        min_z = int(match.group(6))
        max_z = int(match.group(7))
        if min_x < -50 or max_x > 50 or min_y < -50 or max_y > 50 or min_z < -50 or max_z > 50:
            continue
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    space.set((x, y, z), match.group(1) == 'on')
        print(len([c for c in space.non_default_keys() if space.get(c)]))


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
