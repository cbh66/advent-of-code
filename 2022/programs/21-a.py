#!/usr/bin/python3

import sys

def value(name, monkeys):
    operations = monkeys[name]
    if len(monkeys[name]) == 1:
        return int(operations[0])
    [left, operation, right] = operations
    if operation == '+':
        return value(left, monkeys) + value(right, monkeys)
    if operation == '-':
        return value(left, monkeys) - value(right, monkeys)
    if operation == '*':
        return value(left, monkeys) * value(right, monkeys)
    if operation == '/':
        return value(left, monkeys) / value(right, monkeys)

def main(inputs):
    monkeys = {}
    for input in inputs:
        [name, operations] = input.split(': ')
        monkeys[name] = operations.split(' ')
    print(value('root', monkeys))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
