import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from advent_of_code.utils import math as aoc_math
from operator import add, mul, sub, truediv


def get_input(file):
    def get_monkey_info(line):
        monkey, yell = line.split(": ")
        return monkey, (int(yell) if yell.isnumeric() else tuple(yell.split()))

    lines = aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    return dict(map(get_monkey_info, lines))


def compute_monkey(monkey, data):
    # recursively compute what monkey yells
    yell = data[monkey]
    if not isinstance(yell, tuple):
        return yell
    # monkey must perform operation first
    monkey1, op, monkey2 = yell
    op = {"+": add, "-": sub, "*": mul, "/": truediv}[op]
    return op(compute_monkey(monkey1, data), compute_monkey(monkey2, data))


@aoc_output.pretty_solution(1)
def part1(data):
    return round(compute_monkey("root", data))


@aoc_output.pretty_solution(2)
def part2(data):
    # let root do monkey1 - monkey2 to use secant method to compute its zero
    # (zero is when monkey = monkey2)
    monkey1, _, monkey2 = data["root"]
    data["root"] = monkey1, "-", monkey2

    # define the actual function to find the zero
    def f(x):
        data["humn"] = x
        return compute_monkey("root", data)

    return round(aoc_math.secant(f, x1=1e6, x2=1e12))


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    print(example)
    assert part1(example) == 152
    assert part2(example) == 301

    data = get_input("input.txt")
    assert part1(data) == 379578518396784
    assert part2(data) == 3353687996514

    print("Test OK")


if __name__ == "__main__":
    test()
