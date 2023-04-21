#!/usr/bin/python3

import sys

def main(inputs):
    depths = [int(i) for i in inputs]
    increases = 0
    for i in range(len(depths) - 1):
        if depths[i] < depths[i + 1]:
            increases += 1
    print(increases)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
