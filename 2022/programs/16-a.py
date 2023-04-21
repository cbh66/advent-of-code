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

# Initial approach: DFS with trying opening or not opening valve at each step
# Took way too long
# Second idea: Make a complete graph from each valve to each other w/ min distance
# Then step from valve to valve, ignoring valves that are already open, using distance
# as the amt of time to travel, and ALWAYS opening the valve at each step

def max_flow_rate(pos, time_left, valves, time_open):
    if time_left <= 0:
        return time_open
    time_open = time_open.copy()

    time_open[pos] = time_left
    max_so_far = time_open
    for next_valve in valves[pos].connections:
        cost = valves[pos].connections[next_valve]
        if time_open[next_valve] == 0:
            max_so_far = max(
                [max_so_far, max_flow_rate(next_valve, time_left - cost - 1, valves, time_open)],
                key=lambda x: flow(valves, x)
            )
    return max_so_far

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
            if source != dest:
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
    time_open = { name: (30 if valves[name].flow_rate == 0 else 0) for name in valves }
    pprint(flow(valves, max_flow_rate('AA', 30, valves, time_open)))

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
