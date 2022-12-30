from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    def get_ranges(line):
        return [list(map(int, range.split("-"))) for range in line.split(",")]

    return aoc_parse.map_by_line(aoc.read_input(2022, 4, file), get_ranges)


@aoc.pretty_solution(1)
def part1(v):
    def range_contained(r1, r2):
        # just check that extremes are contained
        return r1[0] <= r2[0] <= r2[1] <= r1[1] or r2[0] <= r1[0] <= r1[1] <= r2[1]

    return sum(range_contained(r1, r2) for r1, r2 in v)


@aoc.pretty_solution(2)
def part2(v):
    def range_overlap(r1, r2):
        # check one extreme is contained in the other range
        return r1[0] <= r2[0] <= r1[1] or r2[0] <= r1[0] <= r2[1]

    return sum(range_overlap(r1, r2) for r1, r2 in v)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 503
    assert part2(data) == 827
    print("Test OK")


if __name__ == "__main__":
    test()
