from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import search as aoc_search
from advent_of_code.lib import aoc
from collections import defaultdict, deque
from itertools import combinations
import re


def get_input(file):
    # graph will be {valve : list of connected valves}
    graph = defaultdict(list)
    # {valve : flow rate}
    flow_rates = {}
    for line in aoc_parse.as_lines(aoc.read_input(2022, 16, file)):
        res = re.search(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)
        name = res.group(1)
        flow_rates[name] = int(res.group(2))
        graph[name] = res.group(3).split(", ")
    return graph, flow_rates


def compute_solutions(dists, flow_rates, time):
    # solutions is a dictionary {set of open valves: greatest pressure achievable}
    solutions = defaultdict(int)
    # node = position, time left, open valves, pressure
    start = "AA", time, frozenset(), 0
    todo = deque([start])
    # {(position, open valves) : pressure}
    visited = defaultdict(int)
    # why is BFS faster than DFS?
    while todo:
        valve, time, open, pressure = todo.popleft()

        # store even if not finished because in part2 will need non intersecting solutions
        # which wouldn't be considered otherwise
        solutions[open] = max(solutions[open], pressure)

        # at least 1 to move and 1 to open new valve
        if time <= 2:
            continue

        # move to every possible other valve and open it
        for new_valve in dists[valve]:
            # unless has flow 0 or already open
            if new_valve in open or flow_rates[new_valve] == 0:
                continue
            new_open = open | {new_valve}
            new_time = time - dists[valve][new_valve] - 1
            new_pressure = pressure + new_time * flow_rates[new_valve]
            # discard if no time left or state already visited with higher pressure
            # where state is current valve and set of open valves
            if new_time > 0 and visited[(new := (new_valve, new_open))] < new_pressure:
                visited[new] = new_pressure
                todo.append((new_valve, new_time, new_open, new_pressure))
    return solutions


@aoc.pretty_solution(1)
def part1(graph, flow_rates):
    dists = aoc_search.floyd_warshall(graph)
    solutions = compute_solutions(dists, flow_rates, 30)
    return max(solutions.values())


@aoc.pretty_solution(2)
def part2(graph, flow_rates):
    dists = aoc_search.floyd_warshall(graph)
    # basically the two agents are independent because they open different valves.
    # Compute solution for single agent with 26 minutes then just take the max
    # possible sum of the two pressures achieved independently by the agents
    solutions = compute_solutions(dists, flow_rates, 26)
    return max(p1 + p2 for (s1, p1), (s2, p2) in combinations(solutions.items(), 2) if not s1 & s2)


def main():
    data = get_input("input.txt")
    part1(*data)
    part2(*data)


def test():
    example = get_input("example.txt")
    assert part1(*example) == 1651
    assert part2(*example) == 1707

    data = get_input("input.txt")
    assert part1(*data) == 2114
    assert part2(*data) == 2666

    print("Test OK")


if __name__ == "__main__":
    test()
