from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2025, 2, file)
    ranges = []
    for range in raw.split(","):
        range = list(map(int, range.split("-")))
        ranges.append(range)
    return ranges


@aoc.pretty_solution(1)
def part1(data):

    def valid(id):
        id = str(id)
        mid = len(id)//2
        return id[:mid] != id[mid:]

    res = 0
    for lo, hi in data:
        for id in range(lo, hi+1):
            if not valid(id):
                res += id
    return res


@aoc.pretty_solution(2)
def part2(data):

    def valid(id):
        id = str(id)
        for l in range(1, len(id)//2 + 1):
            for i in range(0, len(id), l):
                if id[i:i+l] != id[0:l]:
                    break
            else:
                return False
        return True

    res = 0
    for lo, hi in data:
        for id in range(lo, hi+1):
            if not valid(id):
                res += id
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 38437576669
    assert part2(data) == 49046150754
    print("Test OK")


if __name__ == "__main__":
    main()
