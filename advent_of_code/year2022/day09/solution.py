from advent_of_code.lib import math as aoc_math
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    def get_step(line):
        direction, steps = line.split()
        return direction, int(steps)

    return aoc_parse.map_by_line(aoc.read_input(2022, 9, file), get_step)


def follow(tail, head):
    """Move tail horizontal/vertical/diagonal by 1 to follow head if not adjacent,
    where head and tail are point in the complex integer plane"""
    if abs(tail - head) >= 2:
        tail += aoc_math.sign(head - tail)
    return tail


def solve(data, n):
    # model points in grid as complex (integer) numbers to ease moving
    direction_step = {"R": 1, "L": -1, "U": 1j, "D": -1j}
    # init all knots to 0
    knots = [0] * n
    # use set for visited points
    visited = {knots[-1]}
    # follow instructions step by step
    for direction, steps in data:
        for _ in range(steps):
            # first move the head
            knots[0] += direction_step[direction]
            # every other knot follows the precedent
            for i in range(1, n):
                knots[i] = follow(knots[i], knots[i - 1])
            visited.add(knots[-1])
    return len(visited)


@aoc.pretty_solution(1)
def part1(data):
    return solve(data, 2)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, 10)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example1 = get_input("example1.txt")
    assert part1(example1) == 13
    assert part2(example1) == 1

    example2 = get_input("example2.txt")
    assert part2(example2) == 36

    data = get_input("input.txt")
    assert part1(data) == 5874
    assert part2(data) == 2467

    print("Test OK")


if __name__ == "__main__":
    test()
