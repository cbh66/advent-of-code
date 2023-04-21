#!/usr/bin/python3

import sys

def score(play):
    if play == 'A' or play == 'X':
        return 1
    elif play == 'B' or play == 'Y':
        return 2
    elif play == 'C' or play == 'Z':
        return 3
    else:
        raise

def outcome(them, me):
    if them == me:
        return 3
    elif them == 1:
        if me == 2:
            return 6
        else:
            return 0
    elif them == 2:
        if me == 3:
            return 6
        else:
            return 0
    elif them == 3:
        if me == 1:
            return 6
        else:
            return 0
    else:
        raise

def main(inputs):
    sum = 0
    for [them, me] in [line.split(' ') for line in inputs]:
        ts = score(them)
        ms = score(me)
        sum += ms + outcome(ts, ms)
    print(sum)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
