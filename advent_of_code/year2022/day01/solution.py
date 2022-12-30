from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2022, 1, file)
    return aoc_parse.input_as_list_of_lists(raw, "")


@aoc.pretty_solution(1)
def part1(v):
    return max([sum(cal) for cal in v])


@aoc.pretty_solution(2)
def part2(v, top=3):
    return sum(sorted([sum(cal) for cal in v])[-top:])


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 72240
    assert part2(data) == 210957
    print("Test OK")


if __name__ == "__main__":
    main()
