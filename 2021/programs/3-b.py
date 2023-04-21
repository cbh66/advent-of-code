#!/usr/bin/python3

import sys

def most_common_bit(inputs, index):
    num_ones = sum([1 if inputs[i][index] == '1' else 0 for i in range(len(inputs)) ])
    if (num_ones >= len(inputs) / 2):
        return '1'
    return '0'

def filter_down(inputs, criteria):
    inputs = inputs.copy()
    num_indices = max([len(input) for input in inputs])
    for i in range(num_indices):
        inputs = [input for input in inputs if criteria(inputs, input, i)]
        if (len(inputs) == 1):
            return inputs[0]

def main(inputs):
    ox_gen = filter_down(inputs, lambda remaining, input, i: input[i] == most_common_bit(remaining, i))
    co2_scrub = filter_down(inputs, lambda remaining, input, i: input[i] != most_common_bit(remaining, i))
    print(ox_gen, co2_scrub)
    print(int(ox_gen, 2) * int(co2_scrub, 2))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
