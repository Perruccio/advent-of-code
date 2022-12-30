from functools import reduce

from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    return aoc_parse.as_lines(aoc.read_input(2022, 3, file))


def priority(x):
    """['a', 'z'] -> [1, 26] and ['A', 'Z'] -> [27, 52]"""
    assert x.islower() or x.isupper()
    return 1 + ord(x) - ord("a") if x.islower() else 27 + ord(x) - ord("A")


@aoc.pretty_solution(1)
def part1(v):
    def share_item(line):
        """compute intersection of halves of line"""
        mid = len(line) // 2
        return (set(line[:mid]) & set(line[mid:])).pop()

    return sum([priority(share_item(line)) for line in v])


@aoc.pretty_solution(2)
def part2(v, k=3):
    """compute intersection of 3 consecutive lines"""
    assert len(v) % k == 0
    return sum(
        [
            priority(reduce(lambda x, y: set(x) & set(y), v[i : i + k]).pop())
            for i in range(0, len(v), k)
        ]
    )


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 8123
    assert part2(data) == 2620
    print("Test OK")


if __name__ == "__main__":
    test()
