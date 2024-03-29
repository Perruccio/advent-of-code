import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from statistics import median


@aoc.pretty_solution(1)
def part1(data):
    # problem is min_m \sum_i |m - x_i|
    # set d (\sum_i |m - x_i|) / dm = 0
    # \sum_i sgn(m - x_i) = 0 <=> m = median(x)
    m = round(median(data))
    return sum([abs(x - m) for x in data])


@aoc.pretty_solution(2)
def part2(data):
    # problem is min_m \sum_i |m - x_i|(|m - x_i| + 1) / 2
    # (we used sum_{i = 0}^n = n(n+1)/2)
    # set d(...) / dm = 0
    # by standard manipulation we find m = mean(x) - 1/2 * sum_i sgn(x_i - m) / n
    # (where n = len(x))
    # hence mean(x) - 1/2 <= m <= mean(x) + 1/2
    m1 = sum(data) // len(data)  # floor(mean)

    def fuel(m):
        return sum([abs(x - m) * (abs(x - m) + 1) for x in data]) // 2

    return min(fuel(m1), fuel(m1 + 1))


def main():
    data = list(map(int, aoc_parse.input_as_string(prj_path + '/year2021/input/day07.txt').rstrip().split(',')))
    return part1(data), part2(data)


if __name__ == "__main__":
    main()
