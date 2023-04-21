#!/usr/bin/python3
import sys

ORIENTATIONS = ['>', 'v', '<', '^']

def turn(orientation, direction):
    if direction == 'R':
        return (orientation + 1) % len(ORIENTATIONS)
    elif direction == 'L':
        return (orientation - 1) % len(ORIENTATIONS)

def next_pos(pos, orientation):
    (row, col) = pos
    if orientation == 0:
        col += 1
    elif orientation == 1:
        row += 1
    elif orientation == 2:
        col -= 1
    elif orientation == 3:
        row -= 1
    return (row, col)

def destination(pos, orientation, grid):
    (attempt_row, attempt_col) = next_pos(pos, orientation)
    attempt_row %= len(grid)
    attempt_col %= len(grid[attempt_row])
    while grid[attempt_row][attempt_col] == ' ':
        (attempt_row, attempt_col) = next_pos((attempt_row, attempt_col), orientation)
        attempt_row %= len(grid)
        attempt_col %= len(grid[attempt_row])
    if grid[attempt_row][attempt_col] == '#':
        return pos
    return (attempt_row, attempt_col)

def parse_instructions(text):
    i = 0
    instructions = []
    next_num = ''
    while i < len(text):
        if text[i].isdigit():
            next_num += text[i]
        else:
            if next_num:
                instructions.append(int(next_num))
                next_num = ''
            instructions.append(text[i])
        i += 1
    if next_num:
        instructions.append(int(next_num))
    return instructions

def main(inputs):
    # strip off newline but not spaces
    grid = [line[:-1] for line in inputs[:-2]]
    # pad each line with extra spaces; some are shorter
    max_len = max(len(line) for line in grid)
    grid = [line.ljust(max_len) for line in grid]
    instructions = parse_instructions(inputs[-1].strip())
    orientation = 0
    pos = destination((0, 0), orientation, grid)
    for instr in instructions:
        if isinstance(instr, str):
            orientation = turn(orientation, instr)
        else:
            for i in range(instr):
                (attempt_row, attempt_col) = destination(pos, orientation, grid)
                if grid[attempt_row][attempt_col] == '#':
                    break
                pos = (attempt_row, attempt_col)
    print(pos, orientation)
    (row, col) = pos
    print((1000 * (row + 1)) + (4 * (col + 1)) + orientation)

if __name__ == "__main__":
    main([line for line in sys.stdin.readlines()])
