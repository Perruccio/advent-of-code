from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 4, file)
    return aoc_parse.map_by_line(raw, func=list)


@aoc.pretty_solution(1)
def part1(data):
    ...

@aoc.pretty_solution(2)
def part2(data):
    ...


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("example.txt")
    # assert part1(data) == None
    # assert part2(data) == None
    print("Test OK")


if __name__ == "__main__":
    main()
