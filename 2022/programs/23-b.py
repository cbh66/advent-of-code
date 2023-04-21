#!/usr/bin/python3
import sys
from collections import Counter

def has_neighbors(coords, elf_positions):
    (row, col) = coords
    for d_row in [-1, 0, +1]:
        for d_col in [-1, 0, +1]:
            if (d_row != 0 or d_col != 0) and (row + d_row, col + d_col) in elf_positions:
                return True
    return False

class Elf:
    def __init__(self, coords):
        self.coords = coords
        self.proposed_move = None
        self.first_move_to_consider = 0
        self.considered_moves = [
            ((-1, 0), [(-1, -1), (-1, 0), (-1, +1)]),
            ((+1, 0), [(+1, -1), (+1, 0), (+1, +1)]),
            ((0, -1), [(-1, -1), (0, -1), (+1, -1)]),
            ((0, +1), [(-1, +1), (0, +1), (+1, +1)]),
        ]

    def propose_move(self, elf_positions):
        (row, col) = self.coords
        for i in range(len(self.considered_moves)):
            move_to_consider = (i + self.first_move_to_consider) % len(self.considered_moves)
            ((considered_d_row, considered_d_col), directions_to_check) = self.considered_moves[move_to_consider]
            target = (row + considered_d_row, col + considered_d_col)
            squares_to_check = [(row + d_row, col + d_col) for (d_row, d_col) in directions_to_check]
            if not any(c in elf_positions for c in squares_to_check):
                self.proposed_move = target
                return target

    def move(self):
        if self.proposed_move:
            self.coords = self.proposed_move

    def end_turn(self):
        self.proposed_move = None
        self.first_move_to_consider = (self.first_move_to_consider + 1) % len(self.considered_moves)

def main(inputs):
    elves = [
        Elf((row, col))
        for row in range(len(inputs))
        for col in range(len(inputs[row]))
        if inputs[row][col] == '#'
    ]
    i = 1
    while True:
        positions = { e.coords for e in elves }
        elves_to_move = [e for e in elves if(has_neighbors(e.coords, positions))]
        if len(elves_to_move) == 0:
            break
        move_counts = Counter([e.propose_move(positions) for e in elves_to_move])
        for e in elves_to_move:
            if move_counts[e.proposed_move] == 1:
                e.move()
        for e in elves:
            e.end_turn()
        i += 1
    print(i)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
