#!/usr/bin/python3

import sys

def main(inputs):
    depths = [int(i) for i in inputs]
    windows = [sum(depths[i:i+3]) for i in range(len(depths) - 2)]
    increases = 0
    for i in range(len(windows) - 1):
        if windows[i] < windows[i + 1]:
            increases += 1
    print(increases)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
