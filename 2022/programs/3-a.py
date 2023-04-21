#!/usr/bin/python3

import sys

def score(c):
    return (26 if c.isupper() else 0) + ord(c.lower()) - ord('a') + 1

def main(inputs):
    matching_chars = [
        set(input[:(len(input) // 2)]).intersection(input[(len(input) // 2):])
        for input in inputs
    ]
    print(sum([score(list(c)[0]) for c in matching_chars]))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
