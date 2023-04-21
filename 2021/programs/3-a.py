#!/usr/bin/python3

import sys

def most_common_bit(inputs, index):
    num_ones = sum([1 if inputs[i][index] == '1' else 0 for i in range(len(inputs)) ])
    if (num_ones > len(inputs) / 2):
        return '1'
    return '0'

def main(inputs):
    num_indices = max([len(input) for input in inputs])
    gamma_str = ''.join([most_common_bit(inputs, i) for i in range(num_indices)])
    eps_str = ''.join(['0' if gamma_str[i] == '1' else '1' for i in range(len(gamma_str))])
    print(gamma_str, eps_str)
    print(int(gamma_str, 2) * int(eps_str, 2))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
