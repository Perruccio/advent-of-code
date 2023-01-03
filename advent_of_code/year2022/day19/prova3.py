# pyright: strict
from collections import deque
from dataclasses import dataclass
from advent_of_code.lib import aoc
from enum import IntEnum
from heapq import heappop, heappush
from itertools import count
from typing import Iterable, Iterator, Literal, NamedTuple, Self, TypeAlias


Amount: TypeAlias = int
# The number of robots we have
Robots: TypeAlias = tuple[Amount, Amount, Amount, Amount]
# The number of resources we can build in the time, with the robots we have
Resources: TypeAlias = tuple[Amount, Amount, Amount, Amount]
# the amount of resources the factory requires to build one robot (the factory
# only needs ore, clay and obsidian).
Recipe: TypeAlias = tuple[Amount, Amount, Amount]


class Resource(IntEnum):
    ore = 0
    clay = 1
    obsidian = 2
    geode = 3


class RobotFactoryState(NamedTuple):
    remaining: int
    robots: Robots = (1, 0, 0, 0)
    resources: Resources = (0, 0, 0, 0)

    def traverse(self, bp: "Blueprint") -> Iterator[Self]:
        rem, robots, resources = self.remaining, self.robots, self.resources
        per_robot = zip(Resource, bp.recipes, robots, bp.max_robots, resources)
        # what robot to build next?
        for rtype, recipe, have, rmax, res in per_robot:
            if rmax and have * rem + res >= rmax * rem:
                # factory can't consume more of this resource, no point in
                # producing this type.
                continue
            if not all(bool(prod) for prod, req in zip(robots, recipe) if req):
                # Not all resources can be produced yet
                continue
            # how much time do we need to produce enough of each required resource?
            needed = 1 + (
                max(
                    0 if avail >= req else (req - avail + prod - 1) // prod
                    for req, avail, prod in zip(recipe, resources, robots)
                    if req
                )
            )
            if needed >= rem:  # no time left to build this robot
                continue
            # produce a new state, with the resources that'll be made available
            # by the time the new robot is done minus the resources consumed by
            # the factory to build the new robot, and the new number of robots
            # with this type incremented.
            new_resources = [
                avail - req + prod * needed
                for avail, req, prod in zip(resources, (*recipe, 0), robots)
            ]
            new_robots = list(robots)
            new_robots[rtype] += 1
            yield RobotFactoryState(
                rem - needed, tuple(new_robots), tuple(new_resources)
            )

    @property
    def max_geodes(self) -> Amount:
        """Max geodes this state can produce given the remaining time and built robots"""
        return (
            self.resources[Resource.geode]
            + self.remaining * self.robots[Resource.geode]
        )

    @property
    def max_geode_potential(self) -> Amount:
        """Max geodes this state can produce given the remaining time, built robots, and potential robots"""
        return self.max_geodes + self.remaining * (self.remaining - 1) // 2

    @property
    def priority(self) -> tuple[Amount, Amount, Amount, int]:
        """Priority queue key

        Prioritises states by geodes produced, obsidian produced, clay produced and time remaining.

        """
        return (*(-1 * r for r in self.resources[:0:-1]), self.remaining)


@dataclass(frozen=True)
class Blueprint:
    # the recipe for each robot type
    recipes: tuple[Recipe, Recipe, Recipe, Recipe]
    # the upper limit for each robot, set by the maximum amount of each resource
    # the factory can utilise. (The factory never needs Geode-cracking robots)
    max_robots: tuple[Amount, Amount, Amount, Literal[0]]

    @classmethod
    def from_line(cls, line: str) -> Self:
        # we only need the numbers, that happen to appear on indices that
        # are multiples of 3.
        words = line.split()[6::3]
        recipes = (
            # ore robot, amount of ore
            (int(words[0]), 0, 0),
            # clay robot, amount of ore
            (int(words[2]), 0, 0),
            # obsidian robot, amount of ore and clay
            (int(words[4]), int(words[5]), 0),
            # geode-cracking robot, amount of ore and obsidian
            (int(words[7]), 0, int(words[8])),
        )
        max_robots = [max(resource) for resource in zip(*recipes)]
        return cls(recipes, (*max_robots, 0))  # no limit on the number of geode bots

    def maximum_opened_geodes(self, time: int) -> int:
        start = RobotFactoryState(time)
        queue = deque([start])
        seen = {start}
        max_geodes = 0
        while queue:
            for state in queue.popleft().traverse(self):
                if state in seen or state.max_geode_potential < max_geodes:
                    continue
                max_geodes = max(max_geodes, state.max_geodes)
                seen.add(state)
                queue.append(state)
        return max_geodes


@dataclass
class Factory:
    blueprints: list[Blueprint]

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> Self:
        return cls([Blueprint.from_line(bp) for bp in lines])

    def quality_levels(self, time: int = 24) -> Iterator[int]:
        for i, bp in enumerate(self.blueprints, 1):
            yield prioritised_maximum_opened_geodes(bp, time) * i


example = Factory.from_lines(
    # multi-line blueprints still work as we split by variable-length whitespace.
    """\
Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
""".split(
        "\n\n"
    )
)

@aoc.pretty_solution(1)
def part1():
    return sum(example.quality_levels())



from functools import reduce
from operator import mul


def prioritised_maximum_opened_geodes(bp: Blueprint, t) -> int:
    tiebreaker = count()
    queue: list[tuple[Amount, Amount, Amount, int, int, RobotFactoryState]] = []

    def add(state: RobotFactoryState):
        heappush(queue, (*state.priority, next(tiebreaker), state))

    start = RobotFactoryState(t)
    add(start)
    seen = {start}
    max_geodes = 0
    while queue:
        *_, state = heappop(queue)
        for nstate in state.traverse(bp):
            if nstate in seen or nstate.max_geode_potential < max_geodes:
                continue
            max_geodes = max(max_geodes, nstate.max_geodes)
            seen.add(nstate)
            add(nstate)
    print(f"{len(seen)}")
    return max_geodes


def largest_number_geodes(factory: Factory) -> Iterator[int]:
    for bp in factory.blueprints[:3]:
        yield prioritised_maximum_opened_geodes(bp, 32)

@aoc.pretty_solution(2)
def part2():
    return reduce(mul, largest_number_geodes(example))
    
part1()
part2()