import pathlib

import advent_of_code.utils.aoc as aoc
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse


def get_input(file):
    return aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)


def solve(data, width=40, height=6):
    # substitute "noop" with 0 and "addx x" with 0, x
    # to automatically account for addx being 2 cycles
    shifts = list(map(lambda t: int(t) if t[-1].isdigit() else 0, " ".join(data).split()))
    # init state x and result for part1
    x, res = 1, 0
    # init display
    display = [[False for _ in range(width)] for _ in range(height)]
    for i, dx in enumerate(shifts):
        if (cycle := i + 1) % 40 == 20:
            res += cycle * x
        # lit pixel if crt sees sprite
        display[i // width][i % width] = abs(x - i % width) <= 1
        x += dx
    return res, display


@aoc_output.pretty_solution(1)
def part1(data):
    return solve(data)[0]


@aoc_output.pretty_solution(2)
def part2(data):
    display = solve(data)[1]
    aoc_output.print_image(display)
    # use sum of lit pixels for tests
    return aoc.sum_grid(display)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 13140
    assert part2(example) == 124

    data = get_input("input.txt")
    assert part1(data) == 13920
    assert part2(data) == 94

    print("Test OK")


if __name__ == "__main__":
    test()
