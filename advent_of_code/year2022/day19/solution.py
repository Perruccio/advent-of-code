from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import re
from collections import Counter, defaultdict, deque
from math import prod


class Robot:
    def __init__(self, produce, cost=()):
        self.produce = produce
        self.cost = Counter(cost)


class Blueprint:
    def __init__(self, robots):
        self.robots = robots

    def __iter__(self):
        yield from self.robots

    @classmethod
    def create_blueprint(cls, raw):
        ints = re.findall(aoc_parse.RE["int"], raw)[1:]
        ore_robot = Robot("ore", {"ore": int(ints[0])})
        clay_robot = Robot("clay", {"ore": int(ints[1])})
        obsidian_robot = Robot("obsidian", {"ore": int(ints[2]), "clay": int(ints[3])})
        geode_robot = Robot("geode", {"ore": int(ints[4]), "obsidian": int(ints[5])})
        return cls([ore_robot, clay_robot, obsidian_robot, geode_robot])


def get_input(file):
    return aoc_parse.map_by_line(aoc.read_input(2022, 19, file), Blueprint.create_blueprint)


def is_subset(contained, container):
    return all(container[x] >= contained[x] for x in contained)


def optimize_blueprint(blueprint, time, start_robots):
    # given a resource, compute its theoretically max possible value
    # used for pruning
    def max_possible(resource):
        return resources[resource] + t * robots[resource] + t * (t - 1) / 2

    # compute max useful amount for each resource
    max_ore = max(robot.cost["ore"] for robot in blueprint)
    max_clay = max(robot.cost["clay"] for robot in blueprint)
    max_obsidian = max(robot.cost["obsidian"] for robot in blueprint)
    max_resource = Counter({"ore": max_ore, "clay": max_clay, "obsidian": max_obsidian})

    # for pruning
    geode_robot_cost = next((robot.cost for robot in blueprint if robot.produce == "geode"))
    # state = time_left, resources, robots, robots we are able to build in previous state
    todo = deque([(time, Counter(), start_robots, set())])
    # {state:time} so that we can skip states if already visited with more available time
    visited = defaultdict(int)
    max_geodes = 0
    # dfs
    while todo:
        t, resources, robots, didnt_build = todo.pop()

        # check if over
        if t == 0:
            max_geodes = max(max_geodes, resources["geode"])
            continue

        # if max possible (in very optimistic case) geodes is less than current best,
        # prune this branch. Assume we can build a geode at every moment
        if max_possible("geode") <= max_geodes:
            continue

        # check if state already seen with more time available
        if t <= visited[(new := (tuple(resources.values()), tuple(robots.values())))]:
            continue
        visited[new] = t

        # if won't be ever able to build any more geode robots, compute final score and prune
        if any(max_possible(resource) <= geode_robot_cost[resource] for resource in geode_robot_cost):
            max_geodes = max(max_geodes, resources["geode"] + robots["geode"] * t)
            continue

        t -= 1

        can_build = set()
        # spend resources to build robots
        for robot in blueprint:
            # NB use old resources to check if can build. Build only if previous minute
            # we couldn build it; otherwise it's pointless (the branch where it's been built is better)
            if not is_subset(robot.cost, resources) or robot.produce in didnt_build:
                continue
            # produce if geode or we haven't already too much
            if robot.produce == "geode" or robots[robot.produce] < max_resource[robot.produce]:
                # but add new_resources to new state
                can_build.add(robot.produce)
                todo.append((t, resources - robot.cost + robots, robots + Counter([robot.produce]), set()))

        # pointless to wait if all robots can be built
        if len(can_build) == 4:
            continue

        # add state without building anything, if this is useful.
        if max_resource - resources:
            # appendleft to make best use of optimizations
            todo.appendleft((t, resources + robots, robots, can_build))
    return max_geodes


@aoc.pretty_solution(1)
def part1(data):
    return sum(i * optimize_blueprint(blueprint, 24, Counter(["ore"])) for i, blueprint in enumerate(data, 1))


@aoc.pretty_solution(2)
def part2(data):
    return prod(optimize_blueprint(blueprint, 32, Counter(["ore"])) for blueprint in data[:3])


def main():
    data = get_input("example.txt")
    part1(data)
    # part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 33
    assert part2(example) == 62 * 56

    data = get_input("input.txt")
    assert part1(data) == 1962
    assert part2(data) == 88160

    print("Test OK")


if __name__ == "__main__":
    test()
