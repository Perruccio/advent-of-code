import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def get_neighoburs(i, j, h, w):
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            i2, j2 = i + di, j + dj
            if 0 <= i2 < h and 0 <= j2 < w and (di != 0 or dj != 0):
                yield (i2, j2)

def step(data, h , w):
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

def part1(data):
    h, w = len(data), len(data[0])
    res = 0
    data_copy = [x[:] for x in data]
    for _ in range(100):
        res += step(data_copy, h, w)
    return res

def part2(data):
    h, w = len(data), len(data[0])
    all_flash = False
    steps = 0
    while not all_flash:
        all_flash = step(data, h, w) == h * w
        steps += 1
    return steps

def main(pretty_print = True):
    def map_line(line):
        return [int(x) for x in line]

    data = map_input_lines(prj_path + '/input/day11.txt', map_line)

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()