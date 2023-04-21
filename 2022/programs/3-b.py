#!/usr/bin/python3

import sys

def score(c):
    return (26 if c.isupper() else 0) + ord(c.lower()) - ord('a') + 1

def main(inputs):
    groups = [inputs[i:i+3] for i in range(0, len(inputs), 3)]
    matching_chars = [
        set(a).intersection(set(b)).intersection(set(c))
        for [a, b, c] in groups
    ]
    print(sum([score(list(c)[0]) for c in matching_chars]))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
