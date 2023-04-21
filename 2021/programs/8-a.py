#!/usr/bin/python3

import sys

def main(inputs):
    count = 0
    for input in inputs:
        [patterns, output] = input.split(' | ')
        digits = output.split()
        unique = [digit for digit in digits if len(digit) in [2, 3, 4, 7]]
        count += len(unique)
    print(count)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
