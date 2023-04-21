#!/usr/bin/python3

import sys

CLOSING_TO_OPENING_CHARS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

CLOSING_CHAR_TO_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

class MismatchedDelimeterError(Exception):
    def __init__(self, char, opening_char):
        self.char = char
        self.opening_char = opening_char

def parse(line):
    opening_chars = []
    for char in line:
        if char not in CLOSING_TO_OPENING_CHARS:
            opening_chars.append(char)
        else:
            if len(opening_chars) == 0:
                raise MismatchedDelimeterError(char)
            matching_char = opening_chars.pop()
            if matching_char != CLOSING_TO_OPENING_CHARS[char]:
                raise MismatchedDelimeterError(char, matching_char)

def main(inputs):
    score = 0
    for input in inputs:
        try:
            parse(input)
        except MismatchedDelimeterError as e:
            # print(f'Expected match for {e.opening_char}, got {e.char}')
            score += CLOSING_CHAR_TO_SCORE[e.char]
    print(f'Score = {score}')


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
