import pathlib

curr_dir = pathlib.Path(__file__).parent

import advent_of_code.utils.aoc as aoc


def get_input():
    return aoc.input_as_list_of_lists(str(curr_dir) + "/input.txt", "")


def part1(v):
    return max([sum(cal) for cal in v])


def part2(v, top=3):
    return sum(sorted([sum(cal) for cal in v])[-top:])


def main():
    data = get_input()
    return (aoc.print_result(1, part1, data),
            aoc.print_result(2, part2, data))


def test():
    """test for pytest"""
    assert main() == (72240, 210957)


if __name__ == "__main__":
    main()
