#!/usr/bin/python3

import sys
from pprint import pprint

class BingoSquare:
    def __init__(self, num):
        self._num = num
        self._is_marked = False

    def mark_num(self, num):
        if (self._num == num):
            self._is_marked = True

    def is_marked(self):
        return self._is_marked

    def score(self):
        if not self.is_marked():
            return self._num
        return 0

class BingoBoard:
    def __init__(self, nums):
        self._board = [
            [BingoSquare(num) for num in row]
            for row in nums
        ]
        self._last_called = None

    def mark_num(self, num):
        for row in self._board:
            for square in row:
                square.mark_num(num)
        self._last_called = num

    def has_won(self):
        for i in range(5):
            if self.has_won_row(i) or self.has_won_col(i):
                return True
        return False

    def score(self):
        umnmarked = sum([
            sum([x.score() for x in row])
            for row in self._board
        ])
        return umnmarked * self._last_called

    def has_won_row(self, row):
        for i in range(5):
            if not self._board[row][i].is_marked():
                return False
        return True

    def has_won_col(self, col):
        for i in range(5):
            if not self._board[i][col].is_marked():
                return False
        return True

def play(boards, nums):
    for num in nums:
        for board in boards:
            board.mark_num(num)
        for board in boards:
            if board.has_won():
                return board
        

def main(inputs):
    nums = [int(i) for i in inputs[0].split(',')]
    board_grids = [
        [
            [int(x) for x in line.split()]
            for line in inputs[i:i+5]
        ]
        for i in range(2, len(inputs) - 2, 6)
    ]
    boards = [BingoBoard(grid) for grid in board_grids]
    winner = play(boards, nums)
    print(winner.score())
    

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
