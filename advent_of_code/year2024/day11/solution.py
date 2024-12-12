from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 11, file)
    return aoc_parse.get_ints(raw)


@cache
def compute(n, blinks):
    if blinks == 0:
        return 1
    if n == 0: return compute(1, blinks-1)
    d = aoc_math.n_digits(n)
    if d%2:
        return compute(n*2024, blinks-1)
    q = 10**(d//2)
    return compute(n//q, blinks-1) + compute(n%q, blinks-1)


@aoc.pretty_solution(1)
def part1(data):
    return sum(compute(n, 25) for n in data)


@aoc.pretty_solution(2)
def part2(data):
    return sum(compute(n, 75) for n in data)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 193899
    assert part2(data) == 229682160383225
    print("Test OK")


if __name__ == "__main__":
    main()
