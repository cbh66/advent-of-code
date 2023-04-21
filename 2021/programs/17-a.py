#!/usr/bin/python3

import sys
import re

TARGET_REGEX = re.compile(r'target area: x=(\S+)\.\.(\S+), y=(\S+)\.\.(\S+)')

class Board:
    def __init__(self, x_start, x_end, y_start, y_end, dx, dy):
        self.zero_row = 0
        self.largest_x = x_end
        self.lowest_y = y_start
        self.board = [
            ['.' for _ in range(x_end + 1)]
            for _ in range(self.y_offset(y_start) + 1)
        ]
        for row in range(y_start, y_end + 1):
            for col in range(x_start, x_end + 1):
                self.board[self.y_offset(row)][col] = 'T'
        self.board[0][0] = 'S'
        self.velocity = (dx, dy)
        self.pos = (0, 0)

    # given a y val, returns which row in the board corresponds
    # x vals always map over 1-to-1
    def y_offset(self, val):
        # y values decrease, but row values increase
        return self.zero_row - val

    def next_step(self):
        (x, y) = self.pos
        (dx, dy) = self.velocity
        x += dx
        y += dy
        dx = dx - 1 if dx > 0 else dx + 1 if dx < 0 else 0
        dy -= 1
        self.pos = (x, y)
        self.velocity = (dx, dy)

    def has_overshot(self):
        (x, y) = self.pos
        if x > self.largest_x:
            return True
        if y < self.lowest_y:
            return True
        return False

    def draw(self):
        # first try resizing
        (x, y) = self.pos
        row = self.y_offset(y)
        if row < 0:
            # add enough rows to the top
            self.board = [
                ['.' for _ in range(len(self.board[0]))]
                for _ in range(-row)
            ] + self.board
            self.zero_row -= row
            row = self.y_offset(y) # should be 0 now
        self.board[row][x] = '#'


    def __repr__(self):
        return '\n'.join([
            ''.join(row) for row in self.board
        ])

def main(inputs):
    [box_line, starting_velocity] = inputs
    match = TARGET_REGEX.match(box_line)
    if not match:
        raise Exception('Malformed input')
    x_start, x_end = (int(match.group(1)), int(match.group(2)))
    y_start, y_end = (int(match.group(3)), int(match.group(4)))
    dx, dy = (int(x) for x in starting_velocity.split(','))
    board = Board(x_start, x_end, y_start, y_end, dx, dy)
    while not board.has_overshot():
        board.draw()
        board.next_step()
    print(board)
    print()
    print(f'highest_row={board.zero_row}')

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()][0:2])
