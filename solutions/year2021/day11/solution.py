import pathlib
import aoc.parse
import aoc


def get_neighoburs(i, j, h, w):
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < h and 0 <= j2 < w and (di != 0 or dj != 0):
                yield i2, j2


def step(data, h, w):
    flash = set()
    for i in range(h):
        for j in range(w):
            data[i][j] += 1
            if data[i][j] > 9:
                flash.add((i, j))

    flashed = set()
    while flash:
        flashing = flash.pop()
        for (i, j) in get_neighoburs(flashing[0], flashing[1], h, w):
            data[i][j] += 1
            if data[i][j] > 9 and (i, j) not in flashed:
                flash.add((i, j))
        flashed.add(flashing)

    for (i, j) in flashed:
        data[i][j] = 0

    return len(flashed)


@aoc.pretty_solution(1)
def part1(data):
    h, w = len(data), len(data[0])
    res = 0
    data_copy = [x[:] for x in data]
    for _ in range(100):
        res += step(data_copy, h, w)
    return res


@aoc.pretty_solution(2)
def part2(data):
    h, w = len(data), len(data[0])
    all_flash = False
    steps = 0
    while not all_flash:
        all_flash = step(data, h, w) == h * w
        steps += 1
    return steps


def main():
    def map_line(line):
        return [int(x) for x in line]

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 1659
    assert p2 == 227


if __name__ == "__main__":
    main()
