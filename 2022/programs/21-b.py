#!/usr/bin/python3

import sys

def value(name, monkeys, humn):
    if name == 'humn':
        return humn
    operations = monkeys[name]
    if len(operations) == 1:
        return int(operations[0])
    [left, operation, right] = operations
    if operation == '+':
        return value(left, monkeys, humn) + value(right, monkeys, humn)
    if operation == '-':
        return value(left, monkeys, humn) - value(right, monkeys, humn)
    if operation == '*':
        return value(left, monkeys, humn) * value(right, monkeys, humn)
    if operation == '/':
        return value(left, monkeys, humn) / value(right, monkeys, humn)

def has(monkeys, name, search_val):
    if name == search_val:
        return True
    operations = monkeys[name]
    if len(operations) == 1:
        return False
    [left, op, right] = operations
    return has(monkeys, left, search_val) or has(monkeys, right, search_val)

def bin_search(monkeys):
    [left, op, right] = monkeys['root']
    (static_branch, changing_branch) = (left, right) if has(monkeys, right, 'humn') else (right, left)
    static_val = value(static_branch, monkeys, 0)
    print(f'static: {static_val}')
    (lowest, highest) = (3592056845085, 3592056845087)
    for attempt in [lowest, (lowest + highest) / 2, highest]:
        changing_val = value(changing_branch, monkeys, attempt)
        comparison = 'less' if changing_val < static_val else 'eq' if changing_val == static_val else 'greater'
        print(f'attempt {attempt}: {changing_val} -- {comparison}')

def main(inputs):
    monkeys = {}
    for input in inputs:
        [name, operations] = input.split(': ')
        monkeys[name] = operations.split(' ')
    bin_search(monkeys)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
