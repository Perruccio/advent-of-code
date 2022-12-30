import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


@aoc.pretty_solution(1)
def part1(v):
    return sum(map(int.__lt__, v, v[1:]))


@aoc.pretty_solution(2)
def part2(v, shift=3):
    return sum(map(int.__lt__, v, v[shift:]))


def main():
    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day01.txt', int)
    return part1(data), part2(data)


if __name__ == "__main__":
    main()
