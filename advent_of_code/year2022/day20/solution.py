from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    return aoc_parse.map_by_line(aoc.read_input(2022, 20, file), int)


def solve(data, key=1, times=1):
    # Not my idea. Create a list of indices and mix that.
    # Every time just look for the index and move it according to data.
    # It turns out the searching the index is faster than the straightforward
    # implementation with a list of nodes (of a double-linked list), on which every time we
    # update the links
    n = len(data)
    # data maps original indices to original values
    # indices maps current indices to original indices
    data = list(map(lambda x: x * key, data))
    indices = list(range(n))
    # indices*times = 0, 1, 2, ..., n-1, 0, 1, ...
    for i in indices * times:
        # find current position of index which was originally i
        indices.pop(new_i := indices.index(i))
        # shift it according to data[i] (data is never changed)
        # remember to use mod n-1 because of how jumping in a list works
        indices.insert((new_i + data[i]) % (n - 1), i)

    # find zero
    zero_i = indices.index(data.index(0))
    return sum(data[indices[(zero_i + shift) % n]] for shift in [1000, 2000, 3000])


@aoc.pretty_solution(1)
def part1(data):
    return solve(data)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, key=811589153, times=10)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 3
    assert part2(example) == 1623178306

    data = get_input("input.txt")
    assert part1(data) == 872
    assert part2(data) == 5382459262696

    print("Test OK")


if __name__ == "__main__":
    test()
