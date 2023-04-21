#!/usr/bin/python3

import sys

def main(inputs):
    pos, depth = 0, 0
    for input in inputs:
        instr, dist = input.split()
        if instr == 'forward':
            pos += int(dist)
        elif instr == 'up':
            depth -= int(dist)
        elif instr == 'down':
            depth += int(dist)
    print(f'pos={pos}, depth={depth}')
    print('product', pos * depth)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
