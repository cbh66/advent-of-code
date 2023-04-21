#!/usr/bin/python3

import sys
from pprint import pprint

def main(input):
    answer = max([
        sum([
            int(n)
            for n in chunk.split('\n')
            if n != ''
        ])
        for chunk in input.split('\n\n')
    ])
    pprint(answer)

if __name__ == "__main__":
    main(sys.stdin.read())
