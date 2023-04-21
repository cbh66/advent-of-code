#!/usr/bin/python3

import sys
import re

STEP_REGEX = re.compile(r'(on|off) x=(\S+)\.\.(\S+),y=(\S+)\.\.(\S+),z=(\S+)\.\.(\S+)')            

def first_match(instructions, cuboid, default=False):
    (x_start, x_end, y_start, y_end, z_start, z_end) = cuboid
    for instruction in instructions:
        (ix_start, ix_end, iy_start, iy_end, iz_start, iz_end, val) = instruction
        if (ix_start <= x_start <= x_end <= ix_end + 1 and
            iy_start <= y_start <= y_end <= iy_end + 1 and
            iz_start <= z_start <= z_end <= iz_end + 1):
            return val
    return default

def filter_instructions(instructions, rectangle):
    (x_start, x_end, y_start, y_end) = rectangle
    filtered = []
    for instruction in instructions:
        (ix_start, ix_end, iy_start, iy_end, _, _, _) = instruction
        if (ix_start <= x_start <= x_end <= ix_end + 1 and
            iy_start <= y_start <= y_end <= iy_end + 1):
            filtered.append(instruction)
    return filtered
        


def main(inputs):
    instructions = []
    x_s = set()
    y_s = set()
    z_s = set()
    for input in inputs:
        match = STEP_REGEX.match(input)
        min_x = int(match.group(2))
        max_x = int(match.group(3))
        min_y = int(match.group(4))
        max_y = int(match.group(5))
        min_z = int(match.group(6))
        max_z = int(match.group(7))
        instructions.append((min_x, max_x, min_y, max_y, min_z, max_z, match.group(1) == 'on'))
        x_s.update([min_x, max_x + 1])
        y_s.update([min_y, max_y + 1])
        z_s.update([min_z, max_z + 1])
    x_s = sorted(x_s)
    y_s = sorted(y_s)
    z_s = sorted(z_s)
    count_true = 0
    instructions.reverse()
    for xi in range(len(x_s) - 1):
        x_start = x_s[xi]
        x_end = x_s[xi + 1]
        print(f'x = [{x_start} {x_end}]')
        for yi in range(len(y_s) - 1):
            y_start = y_s[yi]
            y_end = y_s[yi + 1]
            filtered_instructions = filter_instructions(instructions, (x_start, x_end, y_start, y_end))
            for zi in range(len(z_s) - 1):
                z_start = z_s[zi]
                z_end = z_s[zi + 1]
                cuboid  = (x_start, x_end, y_start, y_end, z_start, z_end)
                if first_match(filtered_instructions, cuboid):
                    count_true += (x_end - x_start) * (y_end - y_start) * (z_end - z_start)
    print(count_true)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
