import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
import re
from collections import defaultdict


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

def solve(graph, time_left, pressure=0, start_open=frozenset()):
    # dfs
    # node = (valve, time left, pressure, set of open valves)
    start = ("AA", time_left, pressure, start_open)
    stack = [start]
    max_pressure = pressure
    # store also time left for each visited node, to avoid checking same positions with less time
    visited = defaultdict(int)
    last_open = None
    while stack:
        valve, time, pressure, open = stack.pop()
        if time <= 1:
            if pressure > max_pressure:
                max_pressure = pressure
                last_open = open
            continue
        # any move will cost 1 minute
        new_time = time - 1
        # first choose to open valve if closed (greedy, optimal)
        if valve not in open and graph[valve].flow_rate > 0:
            new_pressure = pressure + new_time * graph[valve].flow_rate
            new_open = open | {valve}
            new_node = valve, new_pressure, new_open
            # node is useful only if never visited or already visited but now we've more time left
            if new_time > visited[new_node]:
                stack.append((valve, new_time, new_pressure, new_open))
                visited[new_node] = new_time
        # move to other valves
        for new_valve in graph[valve].links:
            # node is useful only if never visited or already visited but now we've more time left
            if new_time > visited[(new_node := (new_valve, pressure, open))]:
                stack.append((new_valve, new_time, pressure, open))
                visited[new_node] = new_time

    return max_pressure, last_open


@aoc_output.pretty_solution(1)
def part1(graph):
    return solve(graph, 30)[0]

@aoc_output.pretty_solution(2)
def part2(graph):
    # dfs
    # node = (valve, time left, pressure, set of open valves)
    start = ("AA", 26, 0, frozenset(), 0)
    stack = [start]
    max_pressure = 0
    # store also time left for each visited node, to avoid checking same positions with less time
    visited = defaultdict(int)
    last_open = None
    while stack:
        valve, time, pressure, open, round = stack.pop()
        if time <= 1:
            if pressure > max_pressure:
                max_pressure = pressure
                last_open = open
            if time == 0 and round == 0:
                stack.append(("AA", 26, pressure, open, 1))
            continue
        # any move will cost 1 minute
        new_time = time - 1
        # first choose to open valve if closed (greedy, optimal)
        if valve not in open and graph[valve].flow_rate > 0:
            new_pressure = pressure + new_time * graph[valve].flow_rate
            new_open = open | {valve}
            new_node = valve, new_pressure, new_open, round
            # node is useful only if never visited or already visited but now we've more time left
            if new_time > visited[new_node]:
                stack.append((valve, new_time, new_pressure, new_open, round))
                visited[new_node] = new_time
        # move to other valves
        for new_valve in graph[valve].links:
            # node is useful only if never visited or already visited but now we've more time left
            if new_time > visited[(new_node := (new_valve, pressure, open, round))]:
                stack.append((new_valve, new_time, pressure, open, round))
                visited[new_node] = new_time

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
    assert part2(data) == None

    print("Test OK")


if __name__ == "__main__":
    test()
