import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils.aoc import *


def get_input():
    return input_as_lines(str(curr_dir) + "/input.txt")


def priority(x):
    assert "a" <= x <= "z" or "A" <= x <= "Z"
    return 1 + ord(x) - ord("a") if "a" <= x <= "z" else 27 + ord(x) - ord("A")


def part1(v):
    def share_item(line):
        l = len(line) // 2
        return (set(line[:l]) & set(line[l:])).pop()

    return sum([priority(share_item(line)) for line in v])


def part2(v, k=3):
    assert len(v) % k == 0
    return sum(
        [
            priority((set(v[i]) & set(v[i + 1]) & set(v[i + 2])).pop())
            for i in range(0, len(v), k)
        ]
    )


def main(pretty_print=False):
    data = get_input()
    if pretty_print:
        print_results(1, part1, data), print_results(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main(pretty_print=True)
