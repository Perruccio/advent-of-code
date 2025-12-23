import aoc.parse
from aoc import aoc
from math import lcm


def get_input(file):
    raw = aoc.read_input(2023, 8, file)
    lines = aoc.parse.as_lines(raw)
    # replace L and R with 0 and 1 to be able to easily
    # follow the path
    instructions = list(map(int, lines[0].translate(str.maketrans("LR", "01"))))
    links = {}
    for line in lines[2:]:
        src, dests = line.split(" = ")
        links[src] = dests[1:-1].split(", ")
    return instructions, links


def next_node(node, links, instructions, steps):
    return links[node][instructions[steps % len(instructions)]]


@aoc.pretty_solution(1)
def part1(data):
    instructions, links = data
    curr, end = "AAA", "ZZZ"
    steps = 0
    while curr != end:
        curr = next_node(curr, links, instructions, steps)
        steps += 1
    return steps


@aoc.pretty_solution(2)
def part2(data):
    instructions, graph = data
    is_start = lambda s: s.endswith("A")
    is_end = lambda s: s.endswith("Z")
    # NB it turns out we can assume that
    # after the first time an end node is hit,
    # it always take the same number of steps
    res = 1
    for node in filter(is_start, graph):
        steps = 0
        while not is_end(node):
            node = next_node(node, graph, instructions, steps)
            steps += 1
        # compute lcm of all loops
        res = lcm(res, steps)
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 20221
    assert part2(data) == 14616363770447
    print("Test OK")


if __name__ == "__main__":
    test()
