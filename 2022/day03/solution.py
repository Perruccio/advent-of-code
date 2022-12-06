import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils import aoc
from functools import reduce


def get_input():
    return aoc.input_as_lines(str(curr_dir) + "/input.txt")


def priority(x):
    """['a', 'z'] -> [1, 26] and ['A', 'Z'] -> [27, 52]"""
    assert x.islower() or x.isupper()
    return 1 + ord(x) - ord("a") if x.islower() else 27 + ord(x) - ord("A")


def part1(v):
    def share_item(line):
        """compute intersection of halves of line"""
        mid = len(line) // 2
        return (set(line[:mid]) & set(line[mid:])).pop()

    return sum([priority(share_item(line)) for line in v])


def part2(v, k=3):
    """compute intersection of 3 consecutive lines"""
    assert len(v) % k == 0
    return sum(
        [
            priority(reduce(lambda x, y: set(x) & set(y), v[i : i + k]).pop())
            for i in range(0, len(v), k)
        ]
    )


def main(pretty=False):
    data = get_input()
    return (aoc.output_procedure(1, part1, pretty, data),
            aoc.output_procedure(2, part2, pretty, data))


def test():
    """test for pytest"""
    assert main() == (8123, 2620)


if __name__ == "__main__":
    main()
