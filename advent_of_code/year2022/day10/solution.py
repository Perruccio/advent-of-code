import pathlib
import advent_of_code.utils.aoc as aoc


def get_input(file):
    return aoc.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)


def do_cycle(x, cycle, res, crt, display, width):
    # draw pixel if crt sees the sprite
    if 0 <= abs(crt[1] - x) <= 1:
        display[crt[0]][crt[1]] = True
    # advance crt
    crt = [crt[0], crt[1] + 1] if crt[1] < width - 1 else [crt[0] + 1, 0]
    # update res
    if cycle % 40 == 20:
        res += cycle * x
    return res, crt


def solve(data, width=40, height=6):
    # init cycle and state x
    cycle = 0
    x = 1
    # result for part 1 (signal strength)
    res = 0
    # crt is position of cathodic ray tube
    crt = [0, 0]
    display = [[False for _ in range(width)] for __ in range(height)]
    for line in data:
        # start cycle
        cycle += 1
        # draw pixel, advance crt, update res
        res, crt = do_cycle(x, cycle, res, crt, display, width)
        if line.startswith("addx"):
            cycle += 1
            res, crt = do_cycle(x, cycle, res, crt, display, width)
            x += int(line.split()[1])
    return res, display


@aoc.pretty_solution(1)
def part1(data):
    return solve(data)[0]


@aoc.pretty_solution(2)
def part2(data):
    display = solve(data)[1]
    aoc.print_image(display)
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
