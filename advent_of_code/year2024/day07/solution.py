from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 7, file)
    return aoc_parse.map_by_line(raw, aoc_parse.get_ints)


def check(nums, res, curr, ops):
    # recursion base case
    if not nums:
        return res == curr
    # just brute force all possibilities
    news = (op(curr, nums[0]) for op in ops)
    return any(check(nums[1:], res, new, ops) for new in news)


@aoc.pretty_solution(1)
def part1(data):
    ops = (mul, add)
    return sum(line[0] for line in data if check(line[2:], line[0], line[1], ops))


@aoc.pretty_solution(2)
def part2(data):
    ops = (mul, add, lambda x, y: int(str(x) + str(y)))
    return sum(line[0] for line in data if check(line[2:], line[0], line[1], ops))

def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 2664460013123
    assert part2(data) == 426214131924213

    print("Test OK")


if __name__ == "__main__":
    test()
