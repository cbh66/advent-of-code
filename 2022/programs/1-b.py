#!/usr/bin/python3

import sys
from pprint import pprint

def main(input):
    answer = sum(
        sorted([
            sum([
                int(n)
                for n in chunk.split('\n')
                if n != ''
            ])
            for chunk in input.split('\n\n')
        ])[-3:]
    )
    pprint(answer)

if __name__ == "__main__":
    main(sys.stdin.read())
