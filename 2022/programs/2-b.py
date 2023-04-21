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

def outcome(them, result):
    if result == 'X': # lose
        if them == 'A':
            return 3
        if them == 'B':
            return 1
        if them == 'C':
            return 2
    if result == 'Y': # draw
        return 3 + score(them)
    if result == 'Z': # win
        return 6 + (score(them) % 3) + 1
    raise

def main(inputs):
    sum = 0
    for [them, me] in [line.split(' ') for line in inputs]:
        sum += outcome(them, me)
    print(sum)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
