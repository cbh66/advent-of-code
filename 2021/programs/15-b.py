#!/usr/bin/python3

import sys
from pprint import pprint

class Square:
    def __init__(self, risk):
        self.risk = risk
        self.best_known_path_score = None

    def __repr__(self):
        # return str(self.best_known_path_score)
        return str(self.risk)

def neighbors(min, i, max):
    if min <= i - 1:
        yield i - 1
    if i + 1 <= max:
        yield i + 1

def build_basic_paths(grid):
    grid[0][0].best_known_path_score = 0
    # go thru first row and add score to one on left
    for x in range(1, len(grid[0])):
        grid[0][x].best_known_path_score = grid[0][x].risk + grid[0][x-1].best_known_path_score
    # go thru first col and add score to one above
    for y in range(1, len(grid)):
        grid[y][0].best_known_path_score = grid[y][0].risk + grid[y-1][0].best_known_path_score

    # pprint(grid)
    for y in range(1, len(grid)):
        for x in range(1, len(grid[y])):
            neighbor_scores = [
                grid[y-1][x].best_known_path_score,
                grid[y][x-1].best_known_path_score
            ]
            grid[y][x].best_known_path_score = grid[y][x].risk + min(neighbor_scores)

def improve_scores(grid):
    made_update = False
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            best_score = grid[r][c].best_known_path_score
            for n_r in neighbors(0, r, len(grid) - 1):
                score_from_neightbor = grid[n_r][c].best_known_path_score + grid[r][c].risk
                if score_from_neightbor < best_score:
                    best_score = score_from_neightbor
                    made_update = True
            for n_c in neighbors(0, c, len(grid[r]) - 1):
                score_from_neightbor = grid[r][n_c].best_known_path_score + grid[r][c].risk
                if score_from_neightbor < best_score:
                    best_score = score_from_neightbor
                    made_update = True
            grid[r][c].best_known_path_score = best_score
    return made_update
            
def new_score(orig_score, tile_num):
    score = orig_score + tile_num
    if score > 9:
        return score - 9
    return score

def extend_row(row):
    new_row = []
    for i in range(len(row) * 5):
        index = i % len(row)
        offset = i // len(row)
        new_row.append(Square(new_score(row[index].risk, offset)))
    return new_row

def extend_columns(grid):
    new_grid = []
    for r in range(len(grid) * 5):
        orig_row = r % len(grid)
        new_grid.append(grid[orig_row].copy())
        for c in range(len(new_grid[r])):
            offset = r // len(grid)
            new_grid[r][c] = Square(new_score(grid[orig_row][c].risk, offset))
    return new_grid

def main(inputs):
    grid = extend_columns([
        extend_row([Square(int(c)) for c in row])
        for row in inputs
    ])
    # pprint([''.join([str(c.risk) for c in row]) for row in grid])
    build_basic_paths(grid)
    i = 0
    while(improve_scores(grid)):
        print(i)
        print(grid[-1][-1].best_known_path_score)
        i += 1

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
