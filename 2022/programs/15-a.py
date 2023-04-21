#!/usr/bin/python3

import sys
import re

class RangeBoundary:
    def __init__(self, index, type):
        self.index = index
        self.type = type
    
    def __repr__(self):
        return f'{self.type}: {self.index}'

class Sensor:
    def __init__(self, coords, closest_beacon):
        self.coords = coords
        [x1, y1] = coords
        [x2, y2] = closest_beacon
        self.range = abs(x1 - x2) + abs(y1 - y2)
    
    def range_boundary(self, row):
        [x, y] = self.coords
        dist_to_here = abs(row - y)
        remaining_dist = self.range - dist_to_here
        if remaining_dist < 0: return []
        return [RangeBoundary(x - remaining_dist, 'START'), RangeBoundary(x + remaining_dist + 1, 'END')]

def sensor_gaps_in_row(sensors, row):
    boundaries = [b for s in sensors for b in s.range_boundary(row)]
    boundaries.sort(key=lambda b: b.type, reverse=True) # put starts before ends
    boundaries.sort(key=lambda b: b.index)
    sum = 0
    start = boundaries[0].index
    i = 1
    num_current_overlaps = 1
    while i < len(boundaries):
        if boundaries[i].type == 'START':
            num_current_overlaps += 1
            if num_current_overlaps == 1:
                start = boundaries[i].index
        else:
            num_current_overlaps -= 1
            if num_current_overlaps == 0:
                sum += boundaries[i].index - start
        i += 1
    return sum

pattern = re.compile('Sensor at x=(.*), y=(.*): closest beacon is at x=(.*), y=(.*)')
def main(inputs):
    sensors = []
    beacons = []
    min_x = min_y = max_x = max_y = 0
    for input in inputs:
        match = pattern.fullmatch(input)
        [sensor_x, sensor_y] = [int(match.group(1)), int(match.group(2))]
        [beacon_x, beacon_y] = [int(match.group(3)), int(match.group(4))]
        min_x = min(min_x, sensor_x, beacon_x)
        min_y = min(min_y, sensor_y, beacon_y)
        max_x = max(max_x, sensor_x, beacon_x)
        max_y = max(max_y, sensor_y, beacon_y)
        sensors.append(Sensor([sensor_x, sensor_y], [beacon_x, beacon_y]))
        beacons.append([beacon_x, beacon_y])

    ROW = 2000000
    beacons_in_row = len(set([x for [x, y] in beacons if y == ROW]))
    print(sensor_gaps_in_row(sensors, ROW) - beacons_in_row)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
