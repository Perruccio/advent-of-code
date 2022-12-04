import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils.aoc import *


def get_input():
    def get_ranges(line):
        return [list(map(int, range.split("-"))) for range in line.split(",")]

    return map_input_lines(str(curr_dir) + "/input.txt", get_ranges)


def part1(v):
    def range_contained(r1, r2):
        # just check that extremes are contained
        return r1[0] <= r2[0] <= r2[1] <= r1[1] or r2[0] <= r1[0] <= r1[1] <= r2[1]

    return sum(range_contained(r1, r2) for r1, r2 in v)


def part2(v):
    def range_overlap(r1, r2):
        # check one extreme is contained in the other range
        return r1[0] <= r2[0] <= r1[1] or r2[0] <= r1[0] <= r2[1]

    return sum(range_overlap(r1, r2) for r1, r2 in v)


def main():
    data = get_input()
    return print_results(1, part1, data), print_results(2, part2, data)


def test():
    """test for pytest"""
    assert main() == (503, 827)


if __name__ == "__main__":
    main()