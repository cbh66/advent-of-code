#!/usr/bin/python3

import sys

# idea: just calculate fuel to move to each position
# find min

def sum_to(goal):
    # return sum(range(0, goal + 1))
    return (goal * (goal + 1) // 2)

def fuel_to_move_to(starts, goal):
    return sum([
        sum_to(abs(start - goal))
        for start in starts
    ])

def main(starts):
    starts = sorted([int(i) for i in starts])
    fuel_costs = [
        fuel_to_move_to(starts, i)
        for i in range(min(starts), max(starts) + 1)
    ]
    print(min(fuel_costs))

if __name__ == "__main__":
    main([line.strip().split(',') for line in sys.stdin.readlines()][0])
