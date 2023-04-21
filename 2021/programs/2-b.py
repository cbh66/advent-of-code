#!/usr/bin/python3

import sys

def main(inputs):
    pos, depth, aim = 0, 0, 0
    for input in inputs:
        instr, dist = input.split()
        if instr == 'forward':
            pos += int(dist)
            depth += int(dist) * aim
        elif instr == 'up':
            aim -= int(dist)
        elif instr == 'down':
            aim += int(dist)
    print(f'pos={pos}, depth={depth}')
    print('product', pos * depth)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
