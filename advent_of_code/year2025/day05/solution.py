from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2025, 5, file)
    fresh, availables = raw.split("\n\n")

    fresh_ranges = []
    for line in fresh.splitlines():
        left, right = map(int, line.split("-"))
        fresh_ranges.append([left, right])

    available = []
    for line in availables.splitlines():
        available.append(int(line))
    return fresh_ranges, available


@aoc.pretty_solution(1)
def part1(data):
    fresh_ranges, available = data
    res = 0
    for av in available:
        for left, right in fresh_ranges:
            if left <= av <= right:
                res += 1
                break
    return res


@aoc.pretty_solution(2)
def part2(data):
    fresh_ranges, _ = data

    # merge fresh intervals in disjoint intervals
    fresh_ranges.sort()
    all_merged = []
    # accumulate overlapping ranges in this
    # aux variable last_interval
    last_interval = fresh_ranges[0]
    for fresh in fresh_ranges:
        # done accumulating overlapping intervals
        if last_interval[1] < fresh[0]:
            all_merged.append(last_interval)
            last_interval = fresh
        # merge into a bigger interval
        elif last_interval[1] < fresh[1]:
            last_interval[1] = fresh[1]
    all_merged.append(last_interval)
    
    res = 0
    for fresh in all_merged:
        res += fresh[1] - fresh[0] + 1
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 828
    assert part2(data) == 352681648086146
    print("Test OK")


if __name__ == "__main__":
    main()
