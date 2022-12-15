import pathlib

from advent_of_code.utils import output as aoc_output, parse as aoc_parse
from collections import defaultdict
from advent_of_code.utils import geometry as aoc_geometry


def get_input(file):
    def get_info(line):
        ints = aoc_parse.get_ints(line)
        return (ints[0], ints[1]), (ints[2], ints[3])

    return aoc_parse.map_input_lines(str(pathlib.Path(__file__).parent) + "/" + file, get_info)


def manhattan_distance(a, b):
    return sum(abs(ca - cb) for ca, cb in zip(a, b))


def find_empty_by_y(data, y):
    res = set()
    beacon_in_y = set()
    for sensor, beacon in data:
        xs, ys = sensor
        xb, yb = beacon
        dist_sb = manhattan_distance(sensor, beacon)
        dist_sy = manhattan_distance(sensor, (xs, y))
        delta = dist_sb - dist_sy
        res.update(xs + dx for dx in range(-delta, delta + 1))
        if yb == y:
            beacon_in_y.add(xb)
    return res, beacon_in_y


@aoc_output.pretty_solution(1)
def part1(data, y):
    empty, beacons_in_y = find_empty_by_y(data, y)
    return len(empty - beacons_in_y)


@aoc_output.pretty_solution(2)
def part2(data, limit):

    empty_range = defaultdict(list)
    for sensor, beacon in data:
        xs, ys = sensor
        dist_sb = manhattan_distance(sensor, beacon)
        for dx in range(-dist_sb, dist_sb + 1):
            if 0 <= xs + dx <= limit:
                yy = [max(0, ys - (dist_sb - abs(dx))), min(limit, ys + dist_sb - abs(dx))]
                aoc_geometry.expand1d(empty_range[xs + dx], yy)
    for x in range(limit + 1):
        if len(empty_range[x]) > 1:
            y = empty_range[x][0][-1] + 1
            if y != empty_range[x][1][0]:
                return x * 4000000 + y


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example, 10) == 26
    assert part2(example, 20) == 56000011

    data = get_input("input.txt")
    assert part1(data, 2000000) == 4748135
    assert part2(data, 4000000) == 13743542639657

    print("Test OK")


if __name__ == "__main__":
    test()
