from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 7, file)
    return aoc.parse.map_by_line(raw, aoc.parse.get_ints)


def check(nums, curr, concat=False):
    # recursion base case
    if len(nums) == 1:
        return curr == nums[0]

    # NB we use the trick of going "backwards":
    # start from target value and do operations backwards
    # i.e. a+b=c becomes a=c-b, (a+b)*c = d becomes a = (d/c) - b
    # this is much more efficient because, with these particular operations,
    # the current value must be divisible by the next number to be valid
    # and subtraction cannot generate negative values. so we can prune away
    # many branches

    # backwards
    n = nums[-1]
    news = []
    if curr % n == 0: news.append(curr // n)
    if curr > n: news.append(curr - n)
    # check if curr = something | n (string concatenation)
    if concat and curr % 10**aoc.math.n_digits(n) == n:
        news.append((curr - n)/10**aoc.math.n_digits(n))
    return any(check(nums[:-1], new, concat) for new in news)


@aoc.pretty_solution(1)
def part1(data):
    return sum(line[0] for line in data if check(line[1:], line[0]))


@aoc.pretty_solution(2)
def part2(data):
    return sum(line[0] for line in data if check(line[1:], line[0], 1))


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
