import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from ast import literal_eval


def get_input(file):
    raw = aoc_parse.input_as_string(str(pathlib.Path(__file__).parent) + "/" + file)
    # get rid of empty lines
    lines = raw.replace("\n\n", "\n").split()
    return list(map(literal_eval, lines))


def compare(l, r):
    """Return l - r in given sense"""
    # fmt: odff
    match l, r:
        case int(), int(): return l - r
        case int(), list(): l = [l]
        case list(), int(): r = [r]
    # map performes compare parallel to iterables l and r (like zip)
    # next takes greedily first element available, otherwise default
    return next((res for res in map(compare, l, r) if res), len(l) - len(r))
    # fmt: on


@aoc_output.pretty_solution(1)
def part1(data):
    pairs = (data[i : i + 2] for i in range(0, len(data), 2))
    return sum(i for i, pair in enumerate(pairs, 1) if compare(*pair) < 0)


@aoc_output.pretty_solution(2)
def part2(data):
    x, y = [[2]], [[6]]
    px = 1 + len([1 for i in data if compare(i, x) < 0])
    # NB add also the [[2]] before [[6]]
    py = 2 + len([1 for i in data if compare(i, y) < 0])
    return px * py


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 13
    assert part2(example) == 140

    data = get_input("input.txt")
    assert part1(data) == 5684
    assert part2(data) == 22932

    print("Test OK")


if __name__ == "__main__":
    test()
