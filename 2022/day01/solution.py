import sys
import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)

from utils.aoc import *
from math import prod


def part1(v):
    return max([sum(cal) for cal in v])


def part2(v, top=3):
    return sum(sorted([sum(cal) for cal in v])[-top:])


def main(pretty_print=True):

    data = input_as_list_of_lists(prj_path + "/2022/day01/input.txt", "")

    if pretty_print:
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main()
