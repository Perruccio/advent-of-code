import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def find_most_common_bit(data, i):
    # check if i-th bit (from right) is the most common or not
    # n >> i & 1  takes i-th bit from right
    return 2 * sum(n >> i & 1 for n in data) >= len(data)


@aoc.pretty_solution(1)
def part1(data):
    n = max(n.bit_length() for n in data)

    # compute gamma by summing 2**i if 1 is the most common bit
    gamma = sum(find_most_common_bit(data, i) << i for i in range(n))

    # bitwise xor
    epsilon = gamma ^ int("1" * n, 2)
    return gamma * epsilon


@aoc.pretty_solution(2)
def part2(data):
    n = max(n.bit_length() for n in data)

    def compute_rate(data, most_common):
        # start from leftmost bit
        i = n - 1
        # continue until only one left
        while len(set(data)) > 1:
            # find most common bit, then compute which
            # one to take using xor
            b = find_most_common_bit(data, i) ^ most_common

            # keep values with i-th bit == b
            data = [x for x in data if (x >> i & 1) == b]

            # advance bit position
            i -= 1
        return data[0]

    return compute_rate(data, 1) * compute_rate(data, 0)


def main():
    def map_line(line):
        return int(line, 2)

    data = aoc_parse.map_input_lines(prj_path + "/year2021/input/day03.txt", map_line)
    return part1(data), part2(data)


if __name__ == "__main__":
    main()
