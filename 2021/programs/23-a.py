#!/usr/bin/python3

import sys
import math
from pprint import pprint

def energy_to_move(amphipod):
    if amphipod == 'A':
        return 1
    if amphipod == 'B':
        return 10
    if amphipod == 'C':
        return 100
    if amphipod == 'D':
        return 1000
    raise Exception(f'Unknown type {amphipod}')


# Rooms:
# 0 1    2    3    4    5 6
#     7    9    11   13
#     8    10   12   14

# edges[a][b] is None if not allowed, else a number representing number of steps
# blocks of None are b/c once in the hall, can only move into a room
# TODO: this doesn't account for being blocked by another... may need to list the whole path
edges = [
    # 0     1     2     3     4     5     6     7     8     9     10    11    12    13    14
    [None, None, None, None, None, None, None, 3,    4,    5,    6,    7,    8,    9,    10  ], # 0
    [None, None, None, None, None, None, None, 2,    3,    4,    5,    6,    7,    8,    9   ], # 1
    [None, None, None, None, None, None, None, 2,    3,    2,    3,    4,    5,    6,    7   ], # 2
    [None, None, None, None, None, None, None, 4,    5,    2,    3,    2,    3,    4,    5   ], # 3
    [None, None, None, None, None, None, None, 6,    7,    4,    5,    2,    3,    2,    3   ], # 4
    [None, None, None, None, None, None, None, 8,    9,    6,    7,    4,    5,    2,    3   ], # 5
    [None, None, None, None, None, None, None, 9,    10,   7,    8,    5,    6,    3,    4   ], # 6
    [3,    2,    2,    4,    6,    8,    9,    None, None, None, None, None, None, None, None], # 7
    [4,    3,    3,    5,    7,    9,    10,   None, None, None, None, None, None, None, None], # 8
    [5,    4,    2,    2,    4,    6,    7,    None, None, None, None, None, None, None, None], # 9
    [6,    5,    3,    3,    5,    7,    8,    None, None, None, None, None, None, None, None], # 10
    [7,    6,    4,    2,    2,    4,    5,    None, None, None, None, None, None, None, None], # 11
    [8,    7,    5,    3,    3,    5,    6,    None, None, None, None, None, None, None, None], # 12
    [9,    8,    6,    4,    2,    2,    3,    None, None, None, None, None, None, None, None], # 13
    [10,   9,    7,    5,    3,    3,    4,    None, None, None, None, None, None, None, None], # 14
]
# edge_paths[a][b] is an array of room numbers that have to be clear to make the move, excluding a and b
edge_paths = [
    # 0     1     2     3     4     5     6     7         8           9       10          11        12        13          14
    [None, None, None, None, None, None, None, [1],      [1,7],      [1,2],   [1,2,9],   [1,2,3], [1,2,3,11], [1,2,3,4], [1,2,3,4,13]], # 0
    [None, None, None, None, None, None, None, [],       [7],        [2],     [2,9],     [2,3],   [2,3,11],   [2,3,4],   [2,3,4,13]  ], # 1
    [None, None, None, None, None, None, None, [],       [7],        [],      [9],       [3],     [3,11],     [3,4],     [3,4,13] ], # 2
    [None, None, None, None, None, None, None, [2],      [2,7],      [],      [9],       [],      [11],       [4],       [4,13]   ], # 3
    [None, None, None, None, None, None, None, [2,3],    [2,3,7],    [3],     [3,9],     [],      [11],       [],        [13]   ], # 4
    [None, None, None, None, None, None, None, [2,3,4],  [2,3,4,7],  [3,4],   [3,4,9],   [4],     [4,11],     [],        [13]   ], # 5
    [None, None, None, None, None, None, None, [2,3,4,5],[2,3,4,5,7],[3,4,5], [3,4,5,9], [4,5],   [4,5,11],   [5],       [5,13] ], # 6
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 7
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 8
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 9
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 10
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 11
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 12
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 13
    [None, None, None, None, None, None, None,    None, None, None, None, None, None, None, None], # 14
]
for r1 in range(len(edge_paths)):
    for r2 in range(len(edge_paths[r1])):
        if edge_paths[r1][r2] is not None:
            edge_paths[r2][r1] = edge_paths[r1][r2]

for r1 in range(len(edges)):
    if not len(edges[r1]) == len(edges):
        raise Exception(f'Row {r1} not the right length')
    for r2 in range(len(edges)):
        if edges[r1][r2] != edges[r2][r1]:
            raise Exception(f'Asymmetric edge between {r1} and {r2}')

# example configuration
# starting_configuration = ([None] * 7) + ['B', 'A', 'C', 'D', 'B', 'C', 'D', 'A']
# real input
starting_configuration = ([None] * 7) + ['B', 'D', 'A', 'C', 'A', 'B', 'D', 'C']
ending_configuration = ([None] * 7) + ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']

# memoized by string representation of configuration: str -> int | None
# None means 
cheapest_path_from_config = {
    str(ending_configuration): 0
}


# returns [new_configuration, energy_taken]
def move(configuration, room1, room2):
    configuration = configuration.copy()
    amphipod = configuration[room1]
    configuration[room1] = None
    configuration[room2] = amphipod
    return [configuration, edges[room1][room2] * energy_to_move(amphipod)]


def is_inviting(configuration, amphipod, room):
    if room < 7:
        return True
    if room < 9:
        rooms = configuration[7:9]
        back = configuration[8]
        target = 'A'
    elif room < 11:
        rooms = configuration[9:11]
        back = configuration[10]
        target = 'B'
    elif room < 13:
        rooms = configuration[11:13]
        back = configuration[12]
        target = 'C'
    else:
        rooms = configuration[13:]
        back = configuration[14]
        target = 'D'
    if room % 2 == 1 and back != target:
        # you'll block someone in if you're not moving to the back
        # unless back is already filled
        return False
    return amphipod == target and all(r is None or r is target for r in rooms)


def can_move(configuration, start, destination):
    if edges[start][destination] is None:
        # no path to destination
        return False
    if configuration[destination] is not None:
        # someone's already there
        return False
    if destination < 7 and is_inviting(configuration, configuration[start], start):
        # already home with partner, not going to leave
        # TODO: if partner isn't home, it MAY be possible to leave
        return False 
    if start < 7 and not is_inviting(configuration, configuration[start], destination):
        # moving in from the hall, so won't move in unless it's a good room
        return False
    for intermediate_room in edge_paths[start][destination]:
        if configuration[intermediate_room] is not None:
            # blocked from taking this path
            return False
    return True


# past configuration is a set of str representations -- if contains current, we're in a loop
# and will return infinity
def cheapest_path(configuration, past_configurations=set()):
    # print(f'--- {len(past_configurations)} ---')
    if configuration == ending_configuration:
        return 0
    if str(configuration) in cheapest_path_from_config:
        known_cheapest_path = cheapest_path_from_config[str(configuration)]
        if known_cheapest_path is not None:
            return known_cheapest_path
    if str(configuration) in past_configurations:
        return math.inf

    past_configurations = past_configurations | {str(configuration)}
    cheapest_so_far = math.inf
    
    for start in range(len(configuration)):
        if configuration[start] is not None:
            for destination in range(len(edges[start])):
                if can_move(configuration, start, destination):
                    # print(f'{start} -> {destination}')
                    [new_config, energy_spent] = move(configuration, start, destination)
                    # print(new_config)
                    if energy_spent > cheapest_so_far:
                        continue
                    energy_from_here = energy_spent + cheapest_path(new_config, past_configurations)
                    if energy_from_here < cheapest_so_far:
                        cheapest_so_far = energy_from_here
    # print(f'Found path {cheapest_so_far}')
    cheapest_path_from_config[str(configuration)] = cheapest_so_far
    return cheapest_so_far


    

def main(inputs):
    print(cheapest_path(starting_configuration))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
