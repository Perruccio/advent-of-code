from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 25, file)
    return list(grid.split() for grid in raw.split("\n\n"))


@aoc.pretty_solution(1)
def part1(data):
    pin = len(data[0])
    locks, keys = [], []
    for grid in data:
        if grid[0][0] == ".":
            # key: use zip on grid to get columns,
            # then just map each column to first "#" element
            key = list(map(lambda col: next(pin - i - 1 for i, x in enumerate(col) if x == "#"), zip(*grid)))
            keys.append(key)
        else:
            # lock
            lock = list(map(lambda col: next(i - 1 for i, x in enumerate(col) if x == "."), zip(*grid)))
            locks.append(lock)
    # brute force all pairs
    res = 0
    for lock in locks:
        for key in keys:
            res += all(l + k < pin - 1 for l, k in zip(lock, key))
    return res


def test():
    data = get_input("input.txt")
    assert part1(data) == 2885
    print("Test OK")


if __name__ == "__main__":
    test()
