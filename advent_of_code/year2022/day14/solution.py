from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import math as aoc_math
from advent_of_code.lib.geometry import Point2D
from advent_of_code.lib import aoc


def get_input(file):
    def parse_wall(line):
        ints = aoc_parse.get_ints(line)
        return [Point2D(x, y) for x, y in zip(ints[::2], ints[1::2])]

    return aoc_parse.map_by_line(aoc.read_input(2022, 14, file), parse_wall)


def make_walls(data):
    rocks = set()
    for wall in data:
        # fill every point from edge to edge (included)
        for edge1, edge2 in zip(wall, wall[1:]):
            diff = edge2 - edge1
            dir = aoc_math.sign(diff)
            rocks.update(edge1 + dir * step for step in range(1 + aoc_math.norm(diff, "inf")))
    return rocks


def simulate_sand(rocks, abyss, floor):
    origin = Point2D(500, 0)
    # counter for rest unit of sand
    rest, path = 0, [origin]
    while True:
        # continue from previous last point
        sand = path[-1]
        # down, down-left, down-right in order
        for dx in [0, -1, 1]:
            # add dy (1)
            next_sand = sand + Point2D(dx, 1)
            # check if movement is possible
            if next_sand in rocks or next_sand.y == floor:
                continue
            path.append(next_sand)
            # go on following this path first (dfs)
            break
        else:
            # no movement is possible, rest sand and backtrack
            rest += 1
            rocks.add(sand)
            path.pop()

        # check if over
        if origin in rocks or (floor is None and sand.y > abyss):
            break
    return rest


@aoc.pretty_solution(1)
def part1(data):
    rocks = make_walls(data)
    abyss = max(rock.y for rock in rocks)
    return simulate_sand(rocks, abyss, None)


@aoc.pretty_solution(2)
def part2(data):
    rocks = make_walls(data)
    abyss = max(rock.y for rock in rocks)
    floor = abyss + 2
    return simulate_sand(rocks, abyss, floor)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 24
    assert part2(example) == 93

    data = get_input("input.txt")
    assert part1(data) == 1133
    assert part2(data) == 27566

    print("Test OK")


if __name__ == "__main__":
    test()
