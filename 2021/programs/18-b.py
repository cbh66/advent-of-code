#!/usr/bin/python3

import sys
import ast
import math

def add_to_left(tree, num):
    if not isinstance(tree, list):
        return tree + num
    [left, right] = tree
    return [add_to_left(left, num), right]

def add_to_right(tree, num):
    if not isinstance(tree, list):
        return tree + num
    [left, right] = tree
    return [left, add_to_right(right, num)]

# explodes the leftmost number that can explode
# returns [a, b, exploded] where a,b are num|None. If num, add a to left or b to right
# exploded is boolean for whether explosion happened. If a or b is not None, must be True
# (but can also be True if both are None)
def explode(tree, level=0):
    if not isinstance(tree, list):
        return [None, None, False] # only pairs can explode, not nums
    [left, right] = tree
    if level >= 3: # next level explodes
        if isinstance(left, list):
            tree[0] = 0
            tree[1] = add_to_left(right, left[1])
            return [left[0], None, True]
        elif isinstance(right, list):
            tree[1] = 0
            tree[0] = add_to_right(left, right[0])
            return [None, right[1], True]

    result = explode(left, level + 1)
    if result[0] is not None:
        return result # exploded on left, but nothing to add to the left
    elif result[1] is not None:
        tree[1] = add_to_left(right, result[1])
        return [None, None, True]
    elif result[2]:
        return result

    result = explode(right, level + 1)
    if result[0] is not None:
        tree[0] = add_to_right(left, result[0])
        return [None, None, True]
    return result # either exploded on the right, so nothing for us to add, or didn't explode

# splits leftmost num in tree
# returns [new_tree, did_split]
def split(tree):
    if isinstance(tree, list):
        [new_left, did_split] = split(tree[0])
        if did_split:
            return [[new_left, tree[1]], True]
        [new_right, did_split] = split(tree[1])
        return [[tree[0], new_right], did_split]

    if tree < 10:
        return [tree, False]
    half = tree / 2
    return [[math.floor(half), math.ceil(half)], True]


def copy(tree):
    if isinstance(tree, list):
        [left, right] = tree
        return [copy(left), copy(right)]
    return tree

def reduce(num):
    num = copy(num)
    while True:
        [_, _, exploded] = explode(num)
        if not exploded:
            [num, did_split] = split(num)
            if not did_split:
                return num

def add(n1, n2):
    sum = [n1, n2]
    return reduce(sum)

def magnitude(tree):
    if isinstance(tree, list):
        [left, right] = tree
        return (3 * magnitude(left)) + (2 * magnitude(right))
    return tree


def main(inputs):
    max_magnitude = 0
    for i in range(len(inputs)):
        for j in range(len(inputs)):
            if i != j:
                sum = add(inputs[i], inputs[j])
                sum_magnitude = magnitude(sum)
                if sum_magnitude > max_magnitude:
                    max_magnitude = sum_magnitude
    print(max_magnitude)
    
    

if __name__ == "__main__":
    main([ast.literal_eval(line.strip()) for line in sys.stdin.readlines()])
