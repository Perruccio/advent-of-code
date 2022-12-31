from advent_of_code.lib import aoc
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import math as aoc_math
from copy import deepcopy


def get_input(file):
    raw = aoc_parse.as_lines(aoc.read_input(2022, 24, file))
    # directions map in complex plane. NB up is -1j
    directions = {">": 1, "<": -1, "^": -1j, "v": 1j}
    blizzards, walls = set(), set()
    for r, line in enumerate(raw):
        for c, point in enumerate(line):
            if point == "#":
                # remove first line and first column to ease modulo operations
                walls.add(complex(c - 1, r - 1))
            elif point in directions:
                # remove first line and first column to ease modulo operations
                blizzards.add((complex(c - 1, r - 1), directions[point]))
    # return width and height of actual rectangle where blizzards can move
    # NB assuming only 1 line of walls in each direction...
    return blizzards, walls, len(raw[0]) - 2, len(raw) - 2


def simulate(data, come_back=False):
    # info
    blizzards_0, walls, width, height = deepcopy(data)
    start, end = -1j, width - 1 + height * 1j
    mod = width + 1j * height
    # add walls around start and end to avoid player going out of map
    walls.add(start - 1j)
    walls.add(end + 1j)
    goals = [end, start, end] if come_back else [end]
    positions, t = {start}, 0
    while goals:

        t += 1

        # move all blizzards, starting from original positions.
        # This is useful to use blizzards_t as set of positions, without storing directions
        blizzards_t = {
            aoc_math.complex_modulo(blizz_pos + t * shift, mod) for blizz_pos, shift in blizzards_0
        }

        # move all positions
        positions = {
            pos + shift
            for pos in positions
            for shift in [1, 1j, 0, -1, -1j]
            if pos + shift not in blizzards_t and pos + shift not in walls
        }

        if goals[0] in positions:
            positions = {goals.pop(0)}
    return t


@aoc.pretty_solution(1)
def part1(data):
    return simulate(data)


@aoc.pretty_solution(2)
def part2(data):
    return simulate(data, come_back=True)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 18
    assert part2(example) == 54

    data = get_input("input.txt")
    assert part1(data) == 228
    assert part2(data) == 723

    print("Test OK")


if __name__ == "__main__":
    test()
