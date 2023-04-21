#!/usr/bin/python3

import sys
from pprint import pprint

ALL_LETTERS = set(['a', 'b', 'c', 'd', 'e', 'f', 'g'])

NUM_OUTPUT_MAP = {
    0: set(['a', 'b', 'c', 'e', 'f', 'g']),
    1: set(['c', 'f']),
    2: set(['a', 'c', 'd', 'e', 'g']),
    3: set(['a', 'c', 'd', 'f', 'g']),
    4: set(['b', 'c', 'd', 'f']),
    5: set(['a', 'b', 'd', 'f', 'g']),
    6: set(['a', 'b', 'd', 'e', 'f', 'g']),
    7: set(['a', 'c', 'f']),
    8: ALL_LETTERS.copy(),
    9: set(['a', 'b', 'c', 'd', 'f', 'g'])
}

def get_pattern_for(num, patterns):
    for pattern in patterns:
        if len(NUM_OUTPUT_MAP[num]) == len(pattern):
            return pattern

def is_solved(possibilities):
    for key in possibilities:
        if len(possibilities[key]) > 1:
            return False
    return True

def reconcile_by_len(possibilities, pattern):
    matching_nums = [NUM_OUTPUT_MAP[n] for n in range(10) if len(pattern) == len(NUM_OUTPUT_MAP[n])]
    possible_outputs = set.union(*matching_nums)
    for letter in possible_outputs:
        possibilities[letter] = possibilities[letter].intersection(possible_outputs)
    return possibilities

# Finds 7 and 1, which are unique. The char used by 7 and not 1 must map to a
def find_a(possibilities, patterns):
    seven_chars = set(get_pattern_for(7, patterns))
    one_chars = set(get_pattern_for(1, patterns))
    difference = seven_chars - one_chars
    remaining_char = difference.pop()
    possibilities[remaining_char] = set(['a'])
    for key in possibilities:
        if key != remaining_char:
            possibilities[key] -= set(['a'])
    return possibilities

# 0, 6, and 9 are each missing one char. The one not in 4 is e, the remaining one
# that is in 1 is c, the last must be d
def match_len_6_patterns(possibilities, patterns):
    # nums 0, 6, and 9
    len_6_patterns = [set(pattern) for pattern in patterns if len(pattern) == 6]
    four_chars = set(get_pattern_for(4, patterns))
    one_chars = set(get_pattern_for(1, patterns))
    missing_chars = set.union(*[ALL_LETTERS - pattern for pattern in len_6_patterns])
    e_char = [char for char in missing_chars if char not in four_chars][0]
    c_char = [char for char in missing_chars if char in one_chars and char != e_char][0]
    d_char = [char for char in missing_chars if char not in [e_char, c_char]][0]
    possibilities[e_char] = set(['e'])
    possibilities[c_char] = set(['c'])
    possibilities[d_char] = set(['d'])
    for key in possibilities:
        if key != e_char:
            possibilities[key] -= set(['e'])
        if key != c_char:
            possibilities[key] -= set(['c'])
        if key != d_char:
            possibilities[key] -= set(['d'])
    return possibilities

# 2, 3, and 5 are each missing 2 chars. Of the missing chars, b and e are the only unique ones,
# which can be distinguished by checking which is in 4
def find_b(possibilities, patterns):
    # numbers 2, 3, and 5
    len_5_patterns = [set(pattern) for pattern in patterns if len(pattern) == 5]
    four_chars = set(get_pattern_for(4, patterns))
    for char in ALL_LETTERS:
        has_char = [p for p in len_5_patterns if char in p]
        if len(has_char) == 1:
            # either b or e, compare with 4 to see which
            if char in four_chars:
                possibilities[char] = set(['b'])
                for key in possibilities:
                    if key != char:
                        possibilities[key] -= set(['b'])
    return possibilities

# Must be called after all other wires have been decoded.
# f is the wire in 1 and g is the other one
def find_f_and_g(possibilities, patterns):
    f_and_g_chars = [key for key in possibilities if len(possibilities[key]) > 1]
    one_chars = set(get_pattern_for(1, patterns))
    f_char = [c for c in f_and_g_chars if c in one_chars][0]
    g_char = [c for c in f_and_g_chars if c != f_char][0]
    possibilities[f_char] = set(['f'])
    for key in possibilities:
        if key != f_char:
            possibilities[key] -= set(['f'])
    possibilities[g_char] = set(['g'])
    for key in possibilities:
        if key != g_char:
            possibilities[key] -= set(['g'])
    return possibilities

def mapped_char(possibilities, char):
    # for key in possibilities:
    #     if char in possibilities[key]:
    #         return key
    result = possibilities[char].copy()
    return result.pop()

def number_for_pattern(possibilities, pattern):
    mapped_pattern = set([mapped_char(possibilities, c) for c in pattern])
    # print(pattern, mapped_pattern)
    for num in NUM_OUTPUT_MAP:
        if NUM_OUTPUT_MAP[num] == mapped_pattern:
            return num

# returns the value of output after decoding the patterns
def decode(patterns, output):
    possibilities = { key: ALL_LETTERS.copy() for key in ALL_LETTERS }
    # print('Finding wire a')
    possibilities = find_a(possibilities, patterns)
    # pprint(possibilities)
    # print('Finding wires c, d, and e')
    possibilities = match_len_6_patterns(possibilities, patterns)
    # pprint(possibilities)
    # print('Finding wire b')
    possibilities = find_b(possibilities, patterns)
    # pprint(possibilities)
    # print('Finding wires f and g')
    possibilities = find_f_and_g(possibilities, patterns)
    # pprint(possibilities)

    num = 0
    radix = 1
    for pattern in reversed(output):
        num += radix * number_for_pattern(possibilities, pattern)
        radix *= 10
    return num


def main(inputs):
    sum = 0
    for input in inputs:
        [patterns, output] = input.split(' | ')
        sum += decode(patterns.split(), output.split())
    print(sum)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
