#!/usr/bin/python3

import sys
import re
from pprint import pprint

RULE_REGEX = re.compile(r'(\w\w) -> (\w)')

class FreqCounter:
    def __init__(self):
        self.counts = {}

    def add(self, s, times=1):
        if s not in self.counts:
            self.counts[s] = 0
        self.counts[s] += times

    def sorted_freqs(self):
        return sorted(self.counts.values())

def transform(counter, rules):
    new_counter = FreqCounter()
    for pair in counter.counts:
        c1 = pair[0]
        c2 = pair[1]
        count = counter.counts[pair]
        if pair in rules:
            c_mid = rules[pair]
            new_counter.add(c1 + c_mid, times=count)
            new_counter.add(c_mid + c2, times=count)
        else:
            new_counter.add(pair, times=count)
    return new_counter

def score(counter):
    char_counts = FreqCounter()
    for pair in counter.counts:
        [c1, c2] = pair
        char_counts.add(c1, times=counter.counts[pair])
        char_counts.add(c2, times=counter.counts[pair])
    sorted_freqs = char_counts.sorted_freqs()
    # Discard sorted_freqs[0], since that will be for ' ', which only occurs at start and end
    # Divide by 2 because every other char is double-counted (each is part of 2 pairs)
    return (sorted_freqs[-1] - sorted_freqs[1]) // 2

def main(inputs):
    polymer = inputs[0]
    rules = {}
    for rule_str in inputs[2:]:
        match = RULE_REGEX.match(rule_str)
        if not match:
            print('FAILED TO MATCH', rule_str)
        rules[match.group(1)] = match.group(2)
    
    counter = FreqCounter()
    counter.add(f' {polymer[0]}')
    counter.add(f'{polymer[-1]} ')
    for i in range(1, len(polymer)):
        counter.add(f'{polymer[i-1]}{polymer[i]}')

    for i in range(40):
        counter = transform(counter, rules)
    print(score(counter))


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
