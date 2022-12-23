import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
import re
from collections import defaultdict
import copy


class Valve:
    __slots__ = "name", "flow_rate", "links"

    def __init__(self, name, flow_rate, links):
        self.name = name
        self.flow_rate = flow_rate
        self.links = links

    @classmethod
    def create_valve(cls, raw):
        res = re.search(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", raw)
        name = res.group(1)
        flow_rate = int(res.group(2))
        links = res.group(3).split(", ")
        return cls(name, flow_rate, links)


def get_input(file):
    return {
        valve.name: valve
        for valve in aoc_parse.map_input_lines(
            str(pathlib.Path(__file__).parent) + "/" + file, Valve.create_valve
        )
    }


def compute_solutions(graph, time):
    # res is a dictionary {set of open valves: greatest pressure achievable}
    res = defaultdict(int)
    # position, time left, open valves, pressure
    start = "AA", time, frozenset(), 0
    todo = [start]
    # {node : time left}
    visited = defaultdict(int)
    while todo:
        valve, time, open, pressure = todo.pop()

        res[open] = max(res[open], pressure)
        new_time = time - 1

        if new_time <= 0:
            continue

        # if valve is closed and has flow rate > 0, open it
        if graph[valve].flow_rate > 0 and valve not in open:
            new_open = open | {valve}
            new_pressure = pressure + new_time * graph[valve].flow_rate
            # this state is useful only if not already seen or have more time left
            if visited[(new := (valve, new_open, new_pressure))] < new_time:
                visited[new] = new_time
                todo.append((valve, new_time, new_open, new_pressure))

        # move to next valves
        for new_valve in graph[valve].links:
            new_open = copy.copy(open)
            if visited[(new := (new_valve, new_open, pressure))] < new_time:
                visited[new] = new_time
                todo.append((new_valve, new_time, new_open, pressure))
    return res


@aoc_output.pretty_solution(1)
def part1(graph):
    solutions = compute_solutions(graph, 30)
    return max(solutions.values())


@aoc_output.pretty_solution(2)
def part2(graph):
    solutions = compute_solutions(graph, 26)
    max_pressure = 0
    for solution1, pressure1 in solutions.items():
        for solution2, pressure2 in solutions.items():
            if not (solution1 & solution2):
                max_pressure = max(pressure1 + pressure2, max_pressure)
    return max_pressure


def main():
    data = get_input("example.txt")
    part1(data)
    res, path = part2(data)
    for node in path:
        print(node)


def test():
    example = get_input("example.txt")
    assert part1(example) == 1651
    assert part2(example) == 1707

    data = get_input("input.txt")
    assert part1(data) == 2114
    assert part2(data) == 2666

    print("Test OK")


if __name__ == "__main__":
    test()
