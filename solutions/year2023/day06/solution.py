import aoc.parse
from aoc import aoc
from math import ceil, sqrt, floor

def get_input(file):
    raw = aoc.read_input(2023, 6, file)
    lines = aoc.parse.as_lines(raw)
    times = aoc.parse.get_ints(lines[0])
    dists = aoc.parse.get_ints(lines[1])
    return times, dists


def solve(times, dists):
    res = 1
    for t, d in zip(times, dists):
        sqrt_delta = sqrt(t**2 - 4 * d)
        t1 = floor((t - sqrt_delta) / 2 + 1)
        t2 = ceil((t + sqrt_delta) / 2 - 1)
        res *= t2 - t1 + 1
    return res


@aoc.pretty_solution(1)
def part1(data):
    times, dists = data
    return solve(times, dists)


@aoc.pretty_solution(2)
def part2(data):
    times, dists = data
    times = int(''.join(map(str, times)))
    dists = int(''.join(map(str, dists)))
    return solve([times], [dists])


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 128700
    assert part2(data) == 39594072
    print("Test OK")


if __name__ == "__main__":
    main()
