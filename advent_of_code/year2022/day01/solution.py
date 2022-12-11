import pathlib

from advent_of_code.utils import output as aoc_output, parse as aoc_parse


def get_input(file):
    return aoc_parse.input_as_list_of_lists(str(pathlib.Path(__file__).parent) + "/" + file, "")


def part1(v):
    return max([sum(cal) for cal in v])


def part2(v, top=3):
    return sum(sorted([sum(cal) for cal in v])[-top:])


def main():
    data = get_input("input.txt")
    aoc_output.print_result(1, part1, data)
    aoc_output.print_result(2, part2, data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 72240
    assert part2(data) == 210957
    print("Test OK")


if __name__ == "__main__":
    main()
