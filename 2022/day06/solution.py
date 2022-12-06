import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils import aoc


def get_input():
    return aoc.input_as_string(str(curr_dir) + "/input.txt")


def check_different_chars(s):
    return len(set(s)) == len(s)


def part1(input, k=4):
    for i in range(len(input) - k + 1):
        if check_different_chars(input[i : i + k]):
            return i + k
    raise RuntimeError


def part2(input):
    return part1(input, k=14)


def main(input=None, pretty=False):
    input = input if input else get_input()
    return (aoc.output_procedure(1, part1, pretty, input),
            aoc.output_procedure(2, part2, pretty, input))


def test():
    """test for pytest"""
    assert part1("abcd") == 4
    assert main("bvwbjplbgvbhsrlpgdmjqwftvncz") == (5, 23)
    assert main("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == (11, 26)
    assert main() == (1155, 2789)
    print("Test OK")


if __name__ == "__main__":
    test()
