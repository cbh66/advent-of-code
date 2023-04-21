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

STARTING_POS = (1, 51)
CUBE_SIDE_ASSOCIATIONS = {}

def zip_cube_sides(side1, side2, initial_orientation, final_orientation):
    for square1, square2 in zip(side1, side2):
        CUBE_SIDE_ASSOCIATIONS[square1, initial_orientation] = (square2, final_orientation)
        CUBE_SIDE_ASSOCIATIONS[square2, turn(turn(final_orientation, 'R'), 'R')] = (
            square1,
            turn(turn(initial_orientation, 'L'), 'L')
        )
# example cube
# # A up -> Q down
# zip_cube_sides([(0, c) for c in range(9, 13)], [(4, c) for c in range(4, 0, -1)], 3, 1)
# # B left -> U down
# zip_cube_sides([(r, 8) for r in range(1, 5)], [(4, c) for c in range(5, 9)], 2, 1)
# # C right -> O left
# zip_cube_sides([(r, 13) for r in range(1, 5)], [(r, 17) for r in range(12, 7, -1)], 0, 2)
# # G right -> M down
# zip_cube_sides([(r, 13) for r in range(5, 9)], [(8, c) for c in range(16, 12, -1)], 0, 1)
# # R left -> P up
# zip_cube_sides([(r, 0) for r in range(5, 9)], [(13, c) for c in range(16, 12, -1)], 2, 3)
# # T down -> L up
# zip_cube_sides([(9, c) for c in range(1, 5)], [(13, c) for c in range(12, 8, -1)], 1, 3)
# # X down -> J right
# zip_cube_sides([(9, c) for c in range(5, 9)], [(r, 8) for r in range(12, 8, -1)], 1, 0)

# real input
# T up -> K right
zip_cube_sides([(100, c) for c in range(1, 51)], [(r, 50) for r in range(51, 101)], 3, 0)
# S left -> G right
zip_cube_sides([(r, 0) for r in range(101, 151)], [(r, 50) for r in range(50, 0, -1)], 2, 0)
# W left -> H down
zip_cube_sides([(r, 0) for r in range(151, 201)], [(0, c) for c in range(51, 101)], 2, 1)
# V down -> D down
zip_cube_sides([(201, c) for c in range(1, 51)], [(0, c) for c in range(101, 151)], 1, 1)
# U right -> N up
zip_cube_sides([(r, 51) for r in range(200, 150, -1)], [(151, c) for c in range(100, 50, -1)], 0, 3)
# M right -> A left
zip_cube_sides([(r, 101) for r in range(150, 100, -1)], [(r, 151) for r in range(1, 51)], 0, 2)
# I right -> B up
zip_cube_sides([(r, 101) for r in range(100, 50, -1)], [(51, c) for c in range(150, 100, -1)], 0, 3)

def destination(pos, orientation, grid):
    dest = next_pos(pos, orientation)
    key = (dest, orientation)
    if key not in CUBE_SIDE_ASSOCIATIONS:
        if grid[dest[0]][dest[1]] == ' ':
            print(f'UH OH WARPING TO SPACE FROM {pos}, {ORIENTATIONS[orientation]} to {dest}')
        return key
    (dest_pos, dest_orientation) = CUBE_SIDE_ASSOCIATIONS[key]
    dest_pos = next_pos(dest_pos, dest_orientation)
    return (dest_pos, dest_orientation)

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
    # Add a whitespace buffer around everything
    grid = [' ' * (max_len + 2)] + [' ' + line.ljust(max_len) + ' ' for line in grid] + [' ' * (max_len + 2)]
    instructions = parse_instructions(inputs[-1].strip())
    orientation = 0
    pos = STARTING_POS
    for instr in instructions:
        if isinstance(instr, str):
            orientation = turn(orientation, instr)
        else:
            for i in range(instr):
                ((attempt_row, attempt_col), attempt_orientation) = destination(pos, orientation, grid)
                if grid[attempt_row][attempt_col] == '#':
                    break
                pos = (attempt_row, attempt_col)
                orientation = attempt_orientation
    print(pos, orientation)
    (row, col) = pos
    print((1000 * row) + (4 * col) + orientation)

if __name__ == "__main__":
    main([line for line in sys.stdin.readlines()])
