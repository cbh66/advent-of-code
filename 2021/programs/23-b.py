#!/usr/bin/python3

import sys
import math
import ast
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
# NEW 15   17   19   21
# NEW 16   18   20   22

# edges[a][b] is None if not allowed, else a number representing number of steps
# blocks of None are b/c once in the hall, can only move into a room
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
] + [[None] * 15 for _ in range(8)]

# account for 8 new rooms
for i in range(len(edges)):
    edges[i] += ([None] * 8)

for hall_room in range(7):
    for new_room in range(15, 23, 2):
        energy = edges[hall_room][new_room - 7] + 1
        edges[new_room][hall_room] = energy
        edges[hall_room][new_room] = energy
        new_room += 1
        energy += 1
        edges[new_room][hall_room] = energy
        edges[hall_room][new_room] = energy

# pprint(edges)

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
] + [[None] * 15 for _ in range(8)]
# account for 8 new rooms
for i in range(len(edge_paths)):
    edge_paths[i] += ([None] * 8)

for r1 in range(len(edge_paths)):
    for r2 in range(len(edge_paths[r1])):
        if edge_paths[r1][r2] is not None:
            edge_paths[r2][r1] = edge_paths[r1][r2]

for hall_room in range(7):
    for new_room in range(15, 23, 2):
        path = edge_paths[hall_room][new_room - 7] + [new_room - 7]
        edge_paths[new_room][hall_room] = path
        edge_paths[hall_room][new_room] = path
        new_room += 1
        path = path + [new_room - 1]
        edge_paths[new_room][hall_room] = path
        edge_paths[hall_room][new_room] = path

for r1 in range(len(edges)):
    if not len(edges[r1]) == len(edges):
        raise Exception(f'Row {r1} not the right length')
    for r2 in range(len(edges)):
        if edges[r1][r2] != edges[r2][r1]:
            raise Exception(f'Asymmetric edge between {r1} and {r2}')

# example configuration
starting_configuration = ([None] * 7) + ['B', 'D', 'D', 'A', 'C', 'C', 'B', 'D', 'B', 'B', 'A', 'C', 'D', 'A', 'C', 'A']
# starting_configuration = ([None] * 6) + ['D', 'A', 'A', 'B', 'B', 'C', 'C', None, 'D', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D']
# real input
# starting_configuration = ([None] * 7) + ['B', 'D', 'A', 'C', 'A', 'B', 'D', 'C']
ending_configuration = ([None] * 7) + (['A'] * 2) + (['B'] * 2) + (['C'] * 2) + (['D'] * 2) + (['A'] * 2) + (['B'] * 2) + (['C'] * 2) + (['D'] * 2) 



# returns [new_configuration, energy_taken]
def move(configuration, room1, room2):
    configuration = configuration.copy()
    amphipod = configuration[room1]
    configuration[room1] = None
    configuration[room2] = amphipod
    return [configuration, edges[room1][room2] * energy_to_move(amphipod)]



def rooms(configuration, room):
    if room < 7:
        raise Exception(f'Wrong type of room {room}')
    if room < 9 or 15 <= room < 17:
        rooms = configuration[7:9] + configuration[15:17]
        offset = 0 if room == 7 else 1 if room == 8 else 2 if room == 15 else 3
        target = 'A'
    elif 9 <= room < 11 or 17 <= room < 19:
        rooms = configuration[9:11] + configuration[17:19]
        offset = 0 if room == 9 else 1 if room == 10 else 2 if room == 17 else 3
        target = 'B'
    elif 11 <= room < 13 or 19 <= room < 21:
        rooms = configuration[11:13] + configuration[19:21]
        offset = 0 if room == 11 else 1 if room == 12 else 2 if room == 19 else 3
        target = 'C'
    else:
        rooms = configuration[13:15] + configuration[21:23]
        offset = 0 if room == 13 else 1 if room == 14 else 2 if room == 21 else 3
        target = 'D'
    return [target, [rooms[:offset], rooms[offset], rooms[offset+1:]]]


def can_move(configuration, start, destination):
    if edges[start][destination] is None:
        # no path to destination
        return False
    # print(configuration)
    # print(destination)
    if configuration[destination] is not None:
        # someone's already there
        return False
    if destination < 7:
        [target, [_, room, rooms_behind]] = rooms(configuration, start)
        # can't leave if everyone behind you is home and you are too
        # TODO: not QUITE right technically but maybe close enough
        if configuration[start] == target and all(x == target for x in rooms_behind):
            return False
    else: 
        [target, [_, _, rooms_behind]] = rooms(configuration, destination)
        if (configuration[start] != target):
            # it's not your home
            return False
        if any([(x != target) for x in rooms_behind]):
            # wrong kinds of ppl already in there, won't go in
            # OR there are unoccupied rooms
            return False

    for intermediate_room in edge_paths[start][destination]:
        if configuration[intermediate_room] is not None:
            # blocked from taking this path
            return False
    return True

def print_square(square):
    return square if square is not None else ' '

def print_configuration(configuration):
    squares = [print_square(s) for s in configuration]
    rows = []
    rows.append('#' * 13)
    rows.append(f'#{squares[0]}{squares[1]} {squares[2]} {squares[3]} {squares[4]} {squares[5]}{squares[6]}#')
    rows.append(f'###{squares[7]}#{squares[9]}#{squares[11]}#{squares[13]}###')
    rows.append(f'  #{squares[8]}#{squares[10]}#{squares[12]}#{squares[14]}#  ')
    rows.append(f'  #{squares[15]}#{squares[17]}#{squares[19]}#{squares[21]}#  ')
    rows.append(f'  #{squares[16]}#{squares[18]}#{squares[20]}#{squares[22]}#  ')
    rows.append('  ' + ('#' * 9) + '  ')
    return '\n'.join(rows)

# memoized by string representation of configuration: str -> int | None
# None means 
cheapest_path_from_config = {
    str(ending_configuration): [0
}

# past configuration is a set of str representations -- if contains current, we're in a loop
# return [energy, path]
def cheapest_path(configuration, past_configurations=[], energies=[0]):
    # print(f'--- layer {len(past_configurations)} ---')
    # print(print_configuration(configuration))
    if len(past_configurations) > 100:
        return math.inf
    if configuration == ending_configuration:
        # print('FOUND')
        # print(f'{len(past_configurations)} steps')
        # for c in past_configurations:
        #     print(print_configuration(ast.literal_eval(c)))
        # print(print_configuration(configuration))
        return [0, [ast.literal_eval(c) for c in past_configurations] + [ending_configuration], energies]
    if str(configuration) in cheapest_path_from_config:
        known_cheapest_path = cheapest_path_from_config[str(configuration)]
        if known_cheapest_path is not None:
            return known_cheapest_path
    if str(configuration) in past_configurations:
        return [math.inf, None, None]

    past_configurations = past_configurations + [str(configuration)]
    # pprint(past_configurations)
    cheapest_so_far = math.inf
    best_path = None
    best_energies = None
    
    for start in range(len(configuration)):
        if configuration[start] is not None:
            for destination in range(len(edges[start])):
                if can_move(configuration, start, destination):
                    [new_config, energy_spent] = move(configuration, start, destination)
                    # print(f'{start} -> {destination}')
                    # print(new_config)
                    if energy_spent > cheapest_so_far:
                        continue
                    [energy_from_here, path_from_here, soln_energies] = cheapest_path(new_config, past_configurations, energies + [energy_spent])
                    energy_from_here += energy_spent
                    if energy_from_here < cheapest_so_far:
                        cheapest_so_far = energy_from_here
                        best_path = path_from_here
                        best_energies = soln_energies
    # print(f'Found path {cheapest_so_far}')
    r_val = [cheapest_so_far, best_path, best_energies]
    cheapest_path_from_config[str(configuration)] = r_val
    return r_val
    

def main(inputs):
    [cost, path, energies] = cheapest_path(starting_configuration)
    for i in range(len(path)):
        c = path[i]
        e = energies[i]
        print(e)
        print(print_configuration(c))
    print(f'cost={cost}')

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
