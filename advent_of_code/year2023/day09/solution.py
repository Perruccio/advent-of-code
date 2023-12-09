from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 9, file)
    return aoc_parse.map_by_line(raw, func=aoc_parse.get_ints)


@aoc.pretty_solution(1)
def part1(data):
    res = 0
    for series in data:
        extrapolated = series[-1]
        # we should just add all the last values
        # of the diff series
        while not all(x == series[0] for x in series):
            series = list(b - a for a, b in zip(series, series[1:]))
            extrapolated += series[-1]
        res += extrapolated
    return res


@aoc.pretty_solution(2)
def part2(data):
    res = 0
    for series in data:
        # a   b   c
        #   d   e
        #     f
        # NB the relation is d = b - a => a = b - d
        # but d = e - f ==> a = b - (e - f) = b - e + f - ... + ...
        # the signs alternate
        back_extrapolated = series[0]
        sign = -1
        while not all(x == series[0] for x in series):
            series = list(b - a for a, b in zip(series, series[1:]))
            back_extrapolated += sign * series[0]
            sign *= -1
        res += back_extrapolated
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("example.txt")
    assert part1(data) == 1681758908
    assert part2(data) == 803
    print("Test OK")


if __name__ == "__main__":
    main()
