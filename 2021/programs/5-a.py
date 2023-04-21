#!/usr/bin/python3

import sys

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'{self.start} -> {self.end}'

    def is_horizontal(self):
        return self.start.x == self.end.x

    def is_vertical(self):
        return self.start.y == self.end.y

    def draw(self, plane):
        if self.is_horizontal():
            if self.start.y <= self.end.y:
                for y in range(self.start.y, self.end.y + 1):
                    plane.mark(self.start.x, y)
            else:
                for y in range(self.end.y, self.start.y + 1):
                    plane.mark(self.start.x, y)
        elif self.is_vertical():
            if self.start.x <= self.end.x:
                for x in range(self.start.x, self.end.x + 1):
                    plane.mark(x, self.start.y)
            else:
                for x in range(self.end.x, self.start.x + 1):
                    plane.mark(x, self.start.y)


class Plane:
    def __init__(self, max_x, max_y):
        self._plane = [
            [0 for i in range(max_x + 1)]
            for j in range(max_y + 1)
        ]

    def mark(self, x, y):
        self._plane[y][x] += 1

    def overlaps(self):
        overlaps = []
        for x in range(len(self._plane)):
            for y in range(len(self._plane[x])):
                if self._plane[x][y] > 1:
                    overlaps.append(Coordinate(x, y))
        return overlaps

    def __repr__(self):
        return '\n'.join([
            ''.join([str(i) if i > 0 else '.' for i in self._plane[x]])
            for x in range(len(self._plane))
        ])
        

def main(inputs):
    lines = [
        [input[0].split(','), input[2].split(',')] for input in inputs
    ]
    lines = [
        Line(Coordinate(int(x1), int(y1)), Coordinate(int(x2), int(y2)))
        for [(x1, y1), (x2, y2)] in lines
    ]
    max_x = max([max([line.start.x, line.end.x]) for line in lines])
    max_y = max([max([line.start.y, line.end.y]) for line in lines])
    plane = Plane(max_x, max_y)
    for line in lines:
        line.draw(plane)
    print(len(plane.overlaps()))

if __name__ == "__main__":
    main([line.strip().split() for line in sys.stdin.readlines()])
