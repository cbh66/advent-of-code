#!/usr/bin/python3

import sys

MAX_DAY = 9
GENERATION_SIZE = 7

def to_arr(timers):
    arr = [0] * MAX_DAY
    for timer in timers:
        arr[timer] += 1
    return arr

def reproduce(schools: list):
    num_fish_due = schools.pop(0)  # todo: maybe use deque
    schools.append(num_fish_due)   # new fish made
    schools[GENERATION_SIZE - 1] += num_fish_due  # old fish have 7 days left
    return schools
    

def main(inputs):
    schools = to_arr([int(i) for i in inputs])
    for day in range(256):
        schools = reproduce(schools)
    print(sum(schools))


if __name__ == "__main__":
    main([line.strip().split(',') for line in sys.stdin.readlines()][0])
