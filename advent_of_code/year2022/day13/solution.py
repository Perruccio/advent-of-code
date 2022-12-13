import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from functools import cmp_to_key
from json import loads


def get_input(file):
    raw = aoc_parse.input_as_string(str(pathlib.Path(__file__).parent) + "/" + file)
    lines = raw.replace("\n\n", "\n").split()
    # use json.loads instead of eval for safety
    return list(map(loads, lines))


def compare(a, b):
    """Return a - b in given sense"""
    a_int = isinstance(a, int)
    b_int = isinstance(b, int)
    # both integers
    if a_int and b_int:
        return a - b
    # only one integer (xor)
    if a_int ^ b_int:
        return compare([a], b) if a_int else compare(a, [b])

    # both lists
    for x, y in zip(a, b):
        res = compare(x, y)
        if res != 0:
            return res
    return len(a) - len(b)


@aoc_output.pretty_solution(1)
def part1(data):
    pairs = (data[i : i + 2] for i in range(0, len(data), 2))
    return sum(i for i, pair in enumerate(pairs, 1) if compare(*pair) < 0)


@aoc_output.pretty_solution(2)
def part2(data):
    x, y = [[2]], [[6]]
    data.extend([x, y])
    data.sort(key=cmp_to_key(compare))
    p1 = data.index(x) + 1
    p2 = data.index(y) + 1
    return p1 * p2


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
