from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2025, , file)


@aoc.pretty_solution(1)
def part1(data):


@aoc.pretty_solution(2)
def part2(data):
    pass


def main():
    data = get_input("input.txt")
    part1(deepcopy(data))
    part2(deepcopy(data))


def test():
    data = get_input("input.txt")
    # assert part1(deepcopy(data)) == 
    # assert part2(deepcopy(data)) == 
    print("Test OK")


if __name__ == "__main__":
    main()
