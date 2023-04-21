#!/usr/bin/python3

import sys
import re
from pprint import pprint

RULE_REGEX = re.compile(r'(\w\w) -> (\w)')

def transform(input, rules):
    c1 = input[0]
    c2 = input[1]
    output = c1
    for c in input[1:]:
        c2 = c
        pair = f'{c1}{c2}'
        if pair in rules:
            output = output + rules[pair]
        output = output + c2
        c1 = c2
    return output

def score(str):
    highest_freq = 1
    lowest_freq = len(str)
    for c in set(str):
        freq = str.count(c)
        if freq > highest_freq:
            highest_freq = freq
        if freq < lowest_freq:
            lowest_freq = freq
    return highest_freq - lowest_freq

def main(inputs):
    polymer = inputs[0]
    rules = {}
    for rule_str in inputs[2:]:
        match = RULE_REGEX.match(rule_str)
        if not match:
            print('FAILED TO MATCH', rule_str)
        rules[match.group(1)] = match.group(2)
    
    for i in range(10):
        polymer = transform(polymer, rules)
        # print(len(polymer))
    print(score(polymer))


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
