#!/usr/bin/python3

import sys
from pprint import pprint

class ALU:
    def __init__(self):
        self.registers = { 'w': 0, 'x': 0, 'y': 0, 'z': 0 }

    def input(self, register, val):
        self.registers[register] = int(val)

    def add(self, a, b):
        self.registers[a] += self.registers[b] if b.isalpha() else int(b)

    def multiply(self, a, b):
        self.registers[a] *= self.registers[b] if b.isalpha() else int(b)

    def divide(self, a, b):
        val = self.registers[b] if b.isalpha() else int(b)
        self.registers[a] = int(self.registers[a] / val)

    def modulo(self, a, b):
        self.registers[a] %= self.registers[b] if b.isalpha() else int(b)

    def compare_equals(self, a, b):
        val = self.registers[b] if b.isalpha() else int(b)
        self.registers[a] = 1 if self.registers[a] == val else 0
        

def base_26(num):
    vals = []
    while num > 0:
        vals.append(num % 26)
        num //= 26
    vals.reverse()
    return vals

def run_program(instructions, stdin):
    alu = ALU()
    for instruction in instructions:
        parts = instruction.split()
        if parts[0] == 'inp':
            pprint(base_26(alu.registers['z']))
            input = stdin[0]
            stdin = stdin[1:]
            alu.input(parts[1], input)
            continue
        [instr, a, b] = parts
        if instr == 'add':
            alu.add(a, b)
        elif instr == 'mul':
            alu.multiply(a, b)
        elif instr == 'div':
            alu.divide(a, b)
        elif instr == 'mod':
            alu.modulo(a, b)
        elif instr == 'eql':
            alu.compare_equals(a, b)
        else:
            raise Exception(f'Invalid instruction "{instruction}"')
    return alu.registers


def main(inputs):
    #            abcdefghijklmn
    test_input = 51121176121391
    pprint(run_program(inputs, str(test_input)))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
