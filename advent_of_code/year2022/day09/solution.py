import pathlib
import advent_of_code.utils.aoc as aoc


def get_input(file):
    file_path = str(pathlib.Path(__file__).parent) + "/" + file

    def get_step(line):
        direction, steps = line.split()
        return direction, int(steps)

    return aoc.map_input_lines(file_path, get_step)


def move(point, direction, step=1):
    """Move 2D point to direction by step"""
    assert direction in "RLUD"
    coord = 0 if direction in "RL" else 1
    step = step if direction in "RU" else -step
    point[coord] += step


def is_adjacent(tail, head):
    """Return True iff tail and head are adjacent or coincide in 2D grid"""
    return -1 <= tail[0] - head[0] <= 1 and -1 <= tail[1] - head[1] <= 1


def follow(tail, head):
    """Move tail horizontal/vertical/diagonal by 1
    to follow head if not adjacent"""
    if not is_adjacent(tail, head):
        for i in [0, 1]:
            tail[i] += aoc.sign(head[i] - tail[i])


def solve(data, n):
    # init all knots to 0,0
    knots = [[0, 0] for _ in range(n)]
    # use set for visited points
    visited = {tuple(knots[-1])}
    # follow instructions step by step
    for direction, steps in data:
        for _ in range(steps):
            # first move the head
            move(knots[0], direction)
            # every other knot follows the precedent
            for i in range(1, n):
                follow(knots[i], knots[i - 1])
            visited.add(tuple(knots[-1]))
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
