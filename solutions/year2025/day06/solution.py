from aoc.all import *


def get_input_1(file):
    raw = aoc.read_input(2025, 6, file)
    data = [list(line.rstrip().split()) for line in raw.splitlines()]
    # transpose the lines to get the problems
    return list(zip(*data))


def get_input_2(file):
    raw = aoc.read_input(2025, 6, file)
    return raw.splitlines()


@aoc.pretty_solution(1)
def part1(data):
    res = 0
    for *v, op in data:
        v = map(int, v)
        res += reduce(operator.mul if op == "*" else operator.add, v)
    return res


@aoc.pretty_solution(2)
def part2(data):
    def stupid_find(s, x, start):
        f = s.find(x, start)
        return f if f >= 0 else len(s)+1

    *lines, ops = data
    rows = len(lines)
    res = 0
    for c, op in enumerate(ops):
        if op == " ":
            continue
        # find position of next operation
        c_next = min(stupid_find(ops, "+", c+1), stupid_find(ops, "*", c+1))
        # compute numbers read vertically
        nums = [int(''.join(lines[r][i] for r in range(rows)).replace(" ","")) for i in range(c, c_next-1)]
        res += reduce(operator.mul if op == "*" else operator.add, nums)
    return res


def main():
    part1(get_input_1("input.txt"))
    part2(get_input_2("input.txt"))


def test():
    assert part1(get_input_1("input.txt")) == 5346286649122
    assert part2(get_input_2("input.txt")) == 10389131401929
    print("Test OK")


if __name__ == "__main__":
    main()
