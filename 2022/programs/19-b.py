#!/usr/bin/python3
import sys
import re
import math

NUM_MINUTES = 32
MATERIAL_TO_MAXIMIZE = 'geode'

def max_cost_of_type(costs, type):
    return max(
        [cost for ingredients in costs.values() for (cost, t) in ingredients if t == type],
        default=math.inf
    )

class Cache:
    def __init__(self, costs):
        self.cache = {}
        self.max_costs = { type: max_cost_of_type(costs, type) for type in costs }
        self.max_costs[MATERIAL_TO_MAXIMIZE] = math.inf

    def get(self, resources, robots, time_left):
        key = self.__key__(resources, robots, time_left)
        if key in self.cache:
            return self.cache[key]
        return None

    def add(self, resources, robots, time_left, value):
        key = self.__key__(resources, robots, time_left)
        self.cache[key] = value
        return value

    def __key__(self, resources, robots, time_left):
        resources = { k: min(resources[k], self.max_costs[k]) for k in resources }
        return f'{resources} -- {robots} -- {time_left}'

def can_afford(costs, robot, resources):
    if not robot:
        return True
    for (amt, type) in costs[robot]:
        if resources[type] < amt:
            return False
    return True

def max_geodes(cache, costs, resources, robots, time_left):
    result_already_found = cache.get(resources, robots, time_left)
    if result_already_found:
        return result_already_found
    if time_left <= 0:
        return cache.add(resources, robots, time_left, resources)

    # It takes a turn for each bot to start producing resources, so if we're towards the end
    # there's not enough time for it to impact the final goal
    robots_worth_getting = []
    if time_left >= 2:
        robots_worth_getting.append('geode')
    if time_left >= 3:
        robots_worth_getting.append('obsidian')
    if time_left >= 4:
        robots_worth_getting.append('clay')
    if time_left >= 5:
        robots_worth_getting.append('ore')
    potential_robots = [
        r for r in robots_worth_getting
        if (
            can_afford(costs, r, resources)
            # No point making a new bot if you're already making more of that type than you can spend
            and robots[r] < max_cost_of_type(costs, r)
            # No point making a new bot if you've already got more resource than you can spend
            and resources[r] < time_left * max_cost_of_type(costs, r)
        )
    ]
    # The only time to NOT get a bot is if there's one you can't afford, that you want to
    # save up for
    if not potential_robots or not all(can_afford(costs, bot, resources) for bot in robots_worth_getting):
        potential_robots.append(None)

    max_so_far = { k: 0 for k in resources }
    for next_robot_choice in potential_robots:
        next_resources = resources.copy()
        next_robots = robots.copy()
        if next_robot_choice:
            for (amt, type) in costs[next_robot_choice]:
                next_resources[type] -= amt
        for robot in next_robots:
            next_resources[robot] += next_robots[robot]
        if next_robot_choice:
            next_robots[next_robot_choice] += 1
            
        max_with_this_bot = max_geodes(cache, costs, next_resources, next_robots, time_left - 1)
        max_so_far = max(
            [max_so_far, max_with_this_bot],
            key=lambda x: x[MATERIAL_TO_MAXIMIZE]
        )
    return cache.add(resources, robots, time_left, max_so_far)

LINE_REGEX = re.compile(r'\W*Each (\w*) robot costs (\d+) (\w+)( and (\d+) (\w+))?\W*')
def main(inputs):
    product = 1
    for input in inputs[0:3]:
        [start, formulas] = input.split(':')
        costs = {}
        for formula in formulas.split('.'):
            match = LINE_REGEX.match(formula)
            if match:
                cost = [(int(match[2]), match[3])]
                if len(match.groups()) >= 5 and match[5] and match[6]:
                    cost.append((int(match[5]), match[6]))
                costs[match[1]] = cost
        resources = { rock: 0 for rock in costs }
        robots = { rock: 0 for rock in costs }
        robots['ore'] = 1
        product *= max_geodes(Cache(costs), costs, resources, robots, NUM_MINUTES)[MATERIAL_TO_MAXIMIZE]
    print(product)

if __name__ == "__main__":
    main([line.strip() for line in sys.stdin.readlines()])
