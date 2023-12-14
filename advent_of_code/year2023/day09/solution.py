from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 9, file)
    return aoc_parse.map_by_line(raw, func=aoc_parse.get_ints)


def extrapolate(series):
    # we should just add all the last values
    # of the diff series
    extrapolated = series[-1]
    while not all(x == series[0] for x in series):
        series = list(b - a for a, b in zip(series, series[1:]))
        extrapolated += series[-1]
    return extrapolated


@aoc.pretty_solution(1)
def part1(data):
    return sum(map(extrapolate, data))


@aoc.pretty_solution(2)
def part2(data):
    # a   b   c
    #   d   e
    #     f
    # NB the relation is d = b - a => a = b - d
    # but d = e - f ==> a = b - (e - f) = b - e + f - ... + ...
    # the signs alternate.
    # However, we can just flip the series and extrapolate normally
    return sum(map(extrapolate, [series[::-1] for series in data]))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 1681758908
    assert part2(data) == 803
    print("Test OK")


if __name__ == "__main__":
    test()
