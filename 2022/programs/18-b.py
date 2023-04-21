#!/usr/bin/python3
import sys
from collections import deque

class Piece:
    def __init__(self, coords):
        self._neighbors = set()
        self.coords = coords

    def add_neighbor(self, neighbor):
        self._neighbors.add(neighbor)
        neighbor._neighbors.add(self)

    def num_neighbors(self):
        return len(self._neighbors)

def neighbors(coords):
    for dimension in range(len(coords)):
        for diff in [-1, 1]:
            neighbor_coords = coords.copy()
            neighbor_coords[dimension] += diff
            yield neighbor_coords

class Droplet:
    def __init__(self):
        self._pieces = {}
        self._min_coords = [0, 0, 0]
        self._max_coords = [0, 0, 0]

    def add_piece(self, coords):
        new_piece = Piece(coords)
        self._pieces[self._key(coords)] = new_piece
        for dimension in range(len(coords)):
            self._min_coords[dimension] = min(self._min_coords[dimension], coords[dimension] - 1)
            self._max_coords[dimension] = max(self._max_coords[dimension], coords[dimension] + 1)
        for neighbor_coords in neighbors(coords):
            neighbor_key = self._key(neighbor_coords)
            if neighbor_key in self._pieces:
                self._pieces[neighbor_key].add_neighbor(new_piece)

    def _key(self, coords):
        (x, y, z) = coords
        return f'{x},{y},{z}'

    def _is_in_range(self, coords):
        for dimension in range(len(coords)):
            if not (self._min_coords[dimension] <= coords[dimension] <= self._max_coords[dimension]):
                return False
        return True

    def _coords_exposed_to_air(self):
        exposed = set()
        to_check = deque([self._min_coords])
        while to_check:
            next = to_check.popleft()
            key = self._key(next)
            if key in exposed: # already checked, don't add neighbors again
                continue
            exposed.add(key)
            for neighbor in neighbors(next):
                neighbor_key = self._key(neighbor)
                if self._is_in_range(neighbor) and neighbor_key not in self._pieces:
                    to_check.append(neighbor)
        return exposed
    
    def surface_area(self):
        exposed_coords = self._coords_exposed_to_air()
        return sum(
            len([
                neighbor for neighbor in neighbors(piece.coords)
                if self._key(neighbor) in exposed_coords
            ])
            for piece in self._pieces.values()
        )

def main(inputs):
    droplet = Droplet()
    for input in inputs:
        droplet.add_piece([int(n) for n in input.split(',')])
    print(droplet.surface_area())

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
