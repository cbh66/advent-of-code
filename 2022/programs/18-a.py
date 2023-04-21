#!/usr/bin/python3
import sys

class Piece:
    def __init__(self, coords):
        self._neighbors = set()
        self.coords = coords

    def add_neighbor(self, neighbor):
        self._neighbors.add(neighbor)
        neighbor._neighbors.add(self)

    def num_neighbors(self):
        return len(self._neighbors)

class Droplet:
    def __init__(self):
        self._pieces = {}

    def add_piece(self, coords):
        new_piece = Piece(coords)
        self._pieces[self._key(coords)] = new_piece
        for coord in range(len(coords)):
            for diff in [-1, 1]:
                neighbor_coords = coords.copy()
                neighbor_coords[coord] += diff
                neighbor_key = self._key(neighbor_coords)
                if neighbor_key in self._pieces:
                    self._pieces[neighbor_key].add_neighbor(new_piece)

    def _key(self, coords):
        (x, y, z) = coords
        return f'{x},{y},{z}'
    
    def surface_area(self):
        return sum(6 - piece.num_neighbors() for piece in self._pieces.values())

def main(inputs):
    droplet = Droplet()
    for input in inputs:
        droplet.add_piece([int(n) for n in input.split(',')])
    print(droplet.surface_area())

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
