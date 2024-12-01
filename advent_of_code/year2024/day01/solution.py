from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from collections import Counter


def get_input(file):
    raw = aoc.read_input(2024, 1, file)
    locs = aoc_parse.map_by_line(raw, aoc_parse.get_ints)
    v1, v2 = [loc[0] for loc in locs], [loc[1] for loc in locs]
    return v1, v2


@aoc.pretty_solution(1)
def part1(v1, v2):
    return sum(abs(x - y) for x, y in zip(sorted(v1), sorted(v2)))


@aoc.pretty_solution(2)
def part2(v1, v2):
    d1, d2 = Counter(v1), Counter(v2)
    return sum(x1 * t1 * d2[x1] for x1, t1 in d1.items())


def main():
    data = get_input("input.txt")
    part1(*data)
    part2(*data)


def test():
    data = get_input("input.txt")
    assert part1(*data) == 1341714
    assert part2(*data) == 27384707
    print("Test OK")


if __name__ == "__main__":
    test()
