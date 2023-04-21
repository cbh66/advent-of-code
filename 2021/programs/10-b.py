#!/usr/bin/python3

import sys

CLOSING_TO_OPENING_CHARS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

OPENING_TO_CLOSING_CHARS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CLOSING_CHAR_TO_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

class MismatchedDelimeterError(Exception):
    def __init__(self, char, opening_char):
        self.char = char
        self.opening_char = opening_char

# returns the sequence of chars needed to complete the line
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
    return [OPENING_TO_CLOSING_CHARS[char] for char in reversed(opening_chars)]

def completion_string_score(completion_string):
    score = 0
    for char in completion_string:
        score *= 5
        score += CLOSING_CHAR_TO_SCORE[char]
    return score

def middle_score(scores):
    scores.sort()
    return scores[(len(scores) - 1) // 2]

def main(inputs):
    scores = []
    for input in inputs:
        try:
            completion_string = parse(input)
            scores.append(completion_string_score(completion_string))
        except MismatchedDelimeterError as e:
            continue
    print(f'Score = {middle_score(scores)}')


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
