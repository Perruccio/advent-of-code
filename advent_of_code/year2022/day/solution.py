import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse


def get_input(file):
    return aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)


@aoc_output.pretty_solution(1)
def part1(data):
    pass


@aoc_output.pretty_solution(2)
def part2(data):
    pass


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == None
    assert part2(example) == None

    data = get_input("input.txt")
    assert part1(data) == None
    assert part2(data) == None

    print("Test OK")


if __name__ == "__main__":
    main()
