from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import re
from collections import Counter
from math import ceil, prod
import heapq as pq

ORE, CLAY, OBS, GEO = range(4)


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
        ore_robot = Robot(ORE, {ORE: int(ints[0])})
        clay_robot = Robot(CLAY, {ORE: int(ints[1])})
        OBS_robot = Robot(OBS, {ORE: int(ints[2]), CLAY: int(ints[3])})
        geode_robot = Robot(GEO, {ORE: int(ints[4]), OBS: int(ints[5])})
        return cls([ore_robot, clay_robot, OBS_robot, geode_robot])


def get_input(file):
    return aoc_parse.map_by_line(aoc.read_input(2022, 19, file), Blueprint.create_blueprint)


def optimize_blueprint(blueprint, time, start_robots):
    # the optimizations are not my ideas, other solvers take credits
    # compute max useful amount for each resource
    max_ore = max(robot.cost[ORE] for robot in blueprint)
    max_clay = max(robot.cost[CLAY] for robot in blueprint)
    max_OBS = max(robot.cost[OBS] for robot in blueprint)
    max_resource = Counter({ORE: max_ore, CLAY: max_clay, OBS: max_OBS})

    # state = time_left, resources, robots
    # use priority queue to first search states with most geodes, obs, clay, time
    # to make best use of optimizations
    todo = []
    pq.heappush(todo, ((0,), (time, Counter(), start_robots)))
    # {state:time} so that we can skip states if already visited with more available time
    visited = set()
    max_geodes = 0
    while todo:
        t, resources, robots = pq.heappop(todo)[1]

        # consider all possible next robot builds
        for robot in blueprint:
            # check if this robot is useful or I can already satisfy the max possible request of a resource
            if (
                robot.produce != GEO
                and robots[robot.produce] * t + resources[robot.produce] >= max_resource[robot.produce] * t
            ):
                continue

            # check if i have necessary robots to harvest resources to build this robot by only waiting
            if any(robots[resource] == 0 for resource in robot.cost):
                continue

            # i have at least 1 robot for each needed resource. compute how much i have to wait
            # +1 because 1 minute to build robot
            time_to_wait = max((cost - resources[res]) / robots[res] for res, cost in robot.cost.items())
            time_to_wait = 1 + ceil(max(time_to_wait, 0))

            # no time left
            if (new_t := (t - time_to_wait)) <= 0:
                continue

            # check there will be enough time after robot is built
            if robot.produce == CLAY and new_t <= 4:
                continue

            # accumulate resources and spend to build new robot.
            new_resources = Counter(
                {res: resources[res] + robots[res] * time_to_wait - robot.cost[res] for res in range(4)}
            )
            # already take into account future geodes for max score
            if robot.produce == GEO:
                new_resources[GEO] += new_t

            # compute robots in new state (make a copy)
            new_robots = Counter(robots)
            # don't count geodes in robots, actually pointless
            if robot.produce != GEO:
                new_robots[robot.produce] += 1

            # if max possible (in very optimistic case) geodes is less than current best,
            # prune this branch. Assume we can build a geode at every moment
            if new_resources[GEO] + new_t * (new_t - 1) // 2 <= max_geodes:
                continue

            # check not already visited
            if (new := (new_t, tuple(new_resources.values()), tuple(new_robots.values()))) in visited:
                continue

            max_geodes = max(max_geodes, new_resources[GEO])
            visited.add(new)
            pq.heappush(
                todo,
                (
                    (-new_resources[GEO], -new_resources[OBS], -new_resources[CLAY], -new_t),
                    (new_t, new_resources, new_robots),
                ),
            )
    return max_geodes


@aoc.pretty_solution(1)
def part1(data):
    return sum(i * optimize_blueprint(blueprint, 24, Counter([ORE])) for i, blueprint in enumerate(data, 1))


@aoc.pretty_solution(2)
def part2(data):
    return prod(optimize_blueprint(blueprint, 32, Counter([ORE])) for blueprint in data[:3])


def main():
    data = get_input("example.txt")
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 33
    assert part2(example) == 3472

    data = get_input("input.txt")
    assert part1(data) == 1962
    assert part2(data) == 88160

    print("Test OK")


if __name__ == "__main__":
    test()
