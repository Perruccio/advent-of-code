import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
import re
from collections import Counter, defaultdict
import copy
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
    return aoc_parse.map_input_lines(
        str(pathlib.Path(__file__).parent) + "/" + file, Blueprint.create_blueprint
    )


def is_subset(counter1, counter2):
    return all(key in counter2 and counter1[key] <= counter2[key] for key in counter1)


def optimize_blueprint(blueprint, time, start_robots):
    max_ore = max(robot.cost["ore"] if "ore" in robot.cost else 0 for robot in blueprint)
    max_clay = max(robot.cost["clay"] if "clay" in robot.cost else 0 for robot in blueprint)
    max_obsidian = max(
        robot.cost["obsidian"] if "obsidian" in robot.cost else 0 for robot in blueprint
    )
    max_resource = {"ore": max_ore, "clay": max_clay, "obsidian": max_obsidian}
    # time_left, resources, robots
    stack = [(time, Counter(), start_robots)]
    visited = defaultdict(lambda: -1)
    max_geodes = 0
    previous_path = {}
    last = None
    while stack:
        time_left, resources, robots = stack.pop()

        if (
            resources["geode"] + robots["geode"] * time_left + time_left * (time_left - 1) // 2
            <= max_geodes
        ):
            continue

        if time_left == 0:
            if resources["geode"] > max_geodes:
                max_geodes = max(max_geodes, resources["geode"])
                last = (time_left, frozenset(resources.items()), frozenset(robots.items()))
            continue
        time_left -= 1

        # first compute collect resources, but remember to build robots with old resources
        new_resource = copy.copy(resources)
        new_resource.update({robot: n for robot, n in robots.items()})

        # add state without building anything
        if time_left > visited[(frozenset(new_resource.items()), frozenset(robots.items()))]:
            stack.append((time_left, copy.copy(new_resource), copy.copy(robots)))
            visited[(frozenset(new_resource.items()), frozenset(robots.items()))] = time_left
            previous_path[
                (time_left, frozenset(new_resource.items()), frozenset(robots.items()))
            ] = (time_left + 1, frozenset(resources.items()), frozenset(robots.items()))

        # spend resources to build robots.
        for robot in blueprint:
            # NB use old resources to check if can build
            if is_subset(robot.cost, resources) and (
                robot.produce == "geode" or robots[robot.produce] < max_resource[robot.produce]
            ):
                # but add new_resources to new state
                new_new_resource = copy.copy(new_resource)
                new_new_resource.subtract(robot.cost)
                new_robots = copy.copy(robots)
                new_robots[robot.produce] += 1
                if (
                    time_left
                    > visited[(frozenset(new_new_resource.items()), frozenset(new_robots.items()))]
                ):
                    stack.append((time_left, new_new_resource, new_robots))
                    visited[
                        (frozenset(new_new_resource.items()), frozenset(new_robots.items()))
                    ] = time_left
                    previous_path[
                        (
                            time_left,
                            frozenset(new_new_resource.items()),
                            frozenset(new_robots.items()),
                        )
                    ] = (time_left + 1, frozenset(resources.items()), frozenset(robots.items()))

    # path = []
    # while last and last in previous_path:
    #     path.append(last)
    #     last = previous_path[last]
    # path = path[::-1]

    # for time, resource, robots in path:
    #     print(f"Time {24 - time}, \t\t {set(resource)=}, \t\t {set(robots)=}")

    # return max_geodes, path
    return max_geodes


@aoc_output.pretty_solution(1)
def part1(data):
    return sum(
        i * optimize_blueprint(blueprint, 24, Counter(["ore"]))
        for i, blueprint in enumerate(data, 1)
    )


@aoc_output.pretty_solution(2)
def part2(data):
    return prod(optimize_blueprint(blueprint, 32, Counter(["ore"])) for blueprint in data[:3])


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


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
