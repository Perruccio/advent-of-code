from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 11, file)
    return aoc_parse.get_ints(raw)


@lru_cache
def blink(n):
    if n == 0:
        return {1:1}
    d = aoc_math.n_digits(n)
    if d % 2 == 0:
        q = 10**(d//2)
        return Counter([n//q, n%q])
    else:
        return {n*2024:1}

def compute(n, blinks):
    v = {n:1}
    for _ in range(blinks):
        v = sum((Counter({a: b*x for a, b in blink(i).items()}) for i, x in v.items()), Counter())
    return sum(v.values())


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
