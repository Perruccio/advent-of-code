from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, dd, file)
    return aoc_parse.as_lines(raw)


@aoc.pretty_solution(1)
def part1(data):
    return


@aoc.pretty_solution(2)
def part2(data):
    return


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    # assert part1(data) == 
    # assert part2(data) == 
    print("Test OK")


if __name__ == "__main__":
    main()
