#!/usr/bin/python3

import sys

def neighbors(min, i, max):
    if min <= i - 1:
        yield i - 1
    if i + 1 <= max:
        yield i + 1

def main(inputs):
    risk_sum = 0
    max_row = len(inputs) - 1
    for row_num in range(len(inputs)):
        row = inputs[row_num]
        max_col = len(row) - 1
        for col_num in range(len(row)):
            lower_neighbors = 0
            for n_r in neighbors(0, row_num, max_row):
                if int(inputs[n_r][col_num]) <= int(inputs[row_num][col_num]):
                    lower_neighbors += 1
            for n_c in neighbors(0, col_num, max_col):
                if int(inputs[row_num][n_c]) <= int(inputs[row_num][col_num]):
                    lower_neighbors += 1
            if lower_neighbors == 0:
                # print('low')
                risk_sum += 1 + int(inputs[row_num][col_num])
    print(risk_sum)


if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
