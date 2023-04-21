#!/usr/bin/python3
import sys
import re
from math import inf
from pprint import pprint

class Valve:
    def __init__(self, flow_rate, connections):
        self.flow_rate = flow_rate
        self.connections = connections

    def __repr__(self):
        return f'{self.flow_rate} -> {self.connections}'

def flow(valves, time_open):
    return sum([valves[v].flow_rate * time_open[v] for v in valves])

# New idea: take part 1 code, but save all unique valve open times
# Then take the max flow for A x B open times

# An alternate idea: once you get to the base case, reset time_left to 26 and rerun for the
# elephant to decide the path it takes in addition to your path
# Might be faster since the elephant chooses from a smaller selection of nodes -- it can only
# choose the same node as the person if it can get there faster
def all_flow_rates(pos, time_left, valves, time_open, flow_rates):
    if time_left <= 0 or time_open[pos] >= time_left or all([time_open[v] > 0 for v in valves]):
        flow_rates.append(time_open)
        return flow_rates
    time_open = time_open.copy()

    time_open[pos] = time_left
    for next_valve in valves[pos].connections:
        cost = valves[pos].connections[next_valve]
        all_flow_rates(next_valve, time_left - cost - 1, valves, time_open, flow_rates)
    return flow_rates

def combine_paths(a, b):
    return { k: max(a[k], b[k]) for k in a }  

def shortest_path_between(source, dest, valves, already_visited):
    if source == dest:
        return 0
    already_visited = already_visited.copy()
    already_visited.add(source)
    min_path = inf
    for neighbor in valves[source].connections:
        if neighbor not in already_visited:
            distance = valves[source].connections[neighbor]
            min_path = min(min_path, distance + shortest_path_between(neighbor, dest, valves, already_visited))
    return min_path

def complete_graph(valves):
    new_valves = {}
    for source in valves:
        connections = {}
        for dest in valves:
            # if source != dest:
                connections[dest] = shortest_path_between(source, dest, valves, set())
        new_valves[source] = Valve(valves[source].flow_rate, connections)
    return new_valves

pattern = re.compile('Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)')
def main(inputs):
    valves = {}
    for input in inputs:
        match = pattern.fullmatch(input)
        valves[match.group(1)] = Valve(int(match.group(2)), { v: 1 for v in match.group(3).split(', ') })
    valves = complete_graph(valves)
    time_open = { name: (30 if valves[name].flow_rate == 0 else 0) for name in valves  }
    time_open['AA'] = 0
    result = all_flow_rates('AA', 26, valves, time_open, [])
    # By sorting, we try the highest scoring solutions first, so we're more likely to find the max earlier.
    # There's about 2.5M solutions in the list, so squaring that is 6.2 trillion possibilities
    # But really we'll probably get the solution in the first few billion, which should only take a few minutes
    result.sort(key=lambda x: flow(valves, x), reverse=True)
    result = result[:500000]
    best_so_far = time_open
    i = 0
    for me in result:
        for elephant in result:
            i += 1
            attempt = combine_paths(me, elephant)
            if flow(valves, attempt) > flow(valves, best_so_far):
                best_so_far = attempt
                print(i, flow(valves, best_so_far))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
