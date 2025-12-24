from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 6, file)
    return raw.splitlines()


@aoc.pretty_solution(1)
def part1(data):
    # split
    data = [line.split() for line in data]
    # transpose
    data = zip(*data)

    res = 0
    for *v, op in data:
        v = map(int, v)
        res += reduce(operator.mul if op == "*" else operator.add, v)
    return res


@aoc.pretty_solution(2)
def part2(data):
    # just transpose before splitting!
    cols = zip(*data)

    # parse the problems by col
    problems = []
    last = []
    for col in cols:
        # accumulate columns of a problem.
        # problems are divided by columns
        # consisting of only spaces
        if set(col) == {" "}:
            problems.append(last)
            last = []
        else:
            last.append(col)
    problems.append(last)

    res = 0
    for problem in problems:
        # NB the operation is now the last element 
        # of first col in problem
        op = problem[0][-1]
        computation = op.join(''.join(col[:-1]) for col in problem)
        res += eval(computation)
    return res


def main():
    part1(get_input("input.txt"))
    part2(get_input("input.txt"))


def test():
    assert part1(get_input("input.txt")) == 5346286649122
    assert part2(get_input("input.txt")) == 10389131401929
    print("Test OK")


if __name__ == "__main__":
    main()
