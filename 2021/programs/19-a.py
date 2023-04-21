#!/usr/bin/python3

import sys
import re
from pprint import pprint

SCANNER_REGEX = re.compile(r'--- scanner (\w) ---')

class Scan:
    def __init__(self, coords):
        self.coords = coords
        self.num_dimensions = min([len(c) for c in coords])
        self._memoize_coords()

    # rotates a single time along the 2 dimensions, keeping other dimensions fixed
    def rotate(self, dim1=0, dim2=1):
        self.coords = [
            [
                -c[dim2] if dim == dim1 else c[dim1] if dim == dim2 else c[dim]
                for dim in range(self.num_dimensions)
            ]
            for c in self.coords
        ]
        self._memoize_coords()

    def _memoize_coords(self):
        self._all_coords = [
            set([c[dim] for c in self.coords])
            for dim in range(self.num_dimensions)
        ]

    # True if there are min_matches coords in the list that match with coords in this scan
    # Else False
    def has_matching_coords(self, min_matches, coords):
        num_matches = 0
        for coord in coords:
            if coord in self:
                num_matches += 1
            if num_matches >= min_matches:
                return True
        return False

    # Tries to add other to this set, if min_matches overlaps can be found
    # Returns True if successful, else false
    def add_if_match(self, other, min_matches):
        # print(other.coords[0])
        offsets = set([
            tuple(anchor[i] - coord[i] for i in range(self.num_dimensions))
            for coord in other.coords
            for anchor in self.coords
        ])
        for offset in offsets:
            offset_coords = [
                [c[dim] + offset[dim] for dim in range(self.num_dimensions)]
                for c in other.coords
            ]
            # print(offset)
            if self.has_matching_coords(min_matches, offset_coords):
                print(f'offset {offset}')
                self._merge(offset_coords)
                return True
        return False

    def __contains__(self, coord):
        for dim in range(self.num_dimensions):
            if coord[dim] not in self._all_coords[dim]:
                return False
        for test_coord in self.coords:
            matches = True
            for i in range(self.num_dimensions):
                if test_coord[i] != coord[i]:
                    matches = False
            if matches:
                return True
        return False

    def _merge(self, coord_list):
        coord_list = [c for c in coord_list if c not in self]
        self.coords += coord_list
        self._memoize_coords()

def add_any_rotation(overall_scan, other_scan, min_matches):
    # https://stackoverflow.com/questions/16452383/how-to-get-all-24-rotations-of-a-3-dimensional-array
    for _ in range(2):
        for _ in range(3):
            other_scan.rotate(0, 1)
            if overall_scan.add_if_match(other_scan, min_matches):
                return True
            for _ in range(3):
                other_scan.rotate(2, 1)
                if overall_scan.add_if_match(other_scan, min_matches):
                    return True
        other_scan.rotate(0, 1)
        other_scan.rotate(2, 1)
        other_scan.rotate(0, 1)
    return False
    
def main(inputs):
    i = 0
    scans = []
    while i < len(inputs):
        # match = SCANNER_REGEX.match(inputs[i])
        i += 1
        coords = []
        while i < len(inputs) and inputs[i]:
            coords.append([int(x) for x in inputs[i].split(',')])
            i += 1
        i += 1
        scans.append(Scan(coords))

    overall_scan = scans[0]
    remaining_scans = scans[1:]
    # print(add_any_rotation(overall_scan, remaining_scans[3], 12))
    for _ in range(1, len(scans)):
        remaining_scans = [
            scan for scan in remaining_scans
            if not add_any_rotation(overall_scan, scan, 12)]
        print(f'{len(remaining_scans)} left')
        print(f'{len(overall_scan.coords)} beacons matched')
        # print(overall_scan.add_if_match(scans[i], 6))


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
