from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import search as aoc_search
from advent_of_code.lib import aoc
from collections import defaultdict
from itertools import combinations
import re


def get_input(file):
    # {valve : list of connected valves}
    graph = defaultdict(list)
    # {valve : flow rate}
    flow_rates = {}
    for line in aoc_parse.as_lines(aoc.read_input(2022, 16, file)):
        res = re.search(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)", line)
        name = res.group(1)
        flow_rates[name] = int(res.group(2))
        graph[name] = res.group(3).split(", ")

    return graph, flow_rates


def preprocess(graph, flow_rates):
    """Remove 0-flow-rate valves from data and use unique powers of 2 instead of valves' names"""
    # NB instead of using actual names of valves, use unique powers of 2.
    # In this way we can very easily and quickly simulate the behaviour of a set using
    # bitwise operations. So we won't need frozenset to keep track of current open valves
    # during BFS

    # assign unique power of 2 to each valve
    remap_valves = {valve: 2**i for i, valve in enumerate(graph)}
    # remap flow rates with powers of 2 and exlude 0-flow-rate valves
    flow_rates = {
        remap_valves[valve]: flow_rate for valve, flow_rate in flow_rates.items() if flow_rate > 0
    }
    # remap graph with powers of 2
    graph = {
        remap_valves[valve]: list(map(remap_valves.__getitem__, links))
        for valve, links in graph.items()
    }

    # use Floyd-Warshall to compute min distance from each node, then remove 0-flow-rate valves
    # and self-connecting links, which are useless to BFS
    dists = aoc_search.floyd_warshall(graph)
    for node, links in dists.items():
        dists[node] = {link: d for link, d in links.items() if link != node and link in flow_rates}

    return remap_valves["AA"], dists, flow_rates


def compute_solutions(start, dists, flow_rates, time):
    # solutions is a dictionary {set of open valves: greatest pressure achievable}
    solutions = defaultdict(int)
    # node = position, time left, sum of open valves (each valve is a power of 2), pressure
    start = start, time, 0, 0
    todo = [start]
    # {(position, open valves) : pressure}
    seen = defaultdict(int)
    # DFS
    while todo:
        valve, time, open, pressure = todo.pop()

        # store even if not finished because in part2 will need non intersecting solutions
        # which wouldn't be considered otherwise
        solutions[open] = max(solutions[open], pressure)

        # at least 1 to move and 1 to open new valve
        if time <= 2:
            continue

        # move to every possible other valve and open it
        for new_valve, dist in dists[valve].items():
            # unless already open. Bitwise and
            if open & new_valve:
                continue

            new_open = open + new_valve
            new_time = time - dist - 1
            new_pressure = pressure + new_time * flow_rates[new_valve]
            # discard if no time left or state (current valve and set of open valves)
            # already visited with higher pressure
            if new_time > 0 and seen[(new := (new_valve, new_open))] < new_pressure:
                seen[new] = new_pressure
                todo.append((new_valve, new_time, new_open, new_pressure))
    return solutions


@aoc.pretty_solution(1)
def part1(graph, flow_rates):
    start, dists, flow_rates = preprocess(graph, flow_rates)
    solutions = compute_solutions(start, dists, flow_rates, 30)
    return max(solutions.values())


@aoc.pretty_solution(2)
def part2(graph, flow_rates):
    start, dists, flow_rates = preprocess(graph, flow_rates)
    # basically the two agents are independent because they open different valves.
    # Compute solution for single agent with 26 minutes then just take the max
    # possible sum of the two pressures achieved independently by the agents
    solutions = compute_solutions(start, dists, flow_rates, 26)
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
