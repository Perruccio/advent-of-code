import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse


def part1(v):
    return sum(map(int.__lt__, v, v[1:]))


def part2(v, shift=3):
    return sum(map(int.__lt__, v, v[shift:]))


def main(pretty_print=True):
    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day01.txt', int)

    if (pretty_print):
        aoc_output.print_result(1, part1, data)
        aoc_output.print_result(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main()
