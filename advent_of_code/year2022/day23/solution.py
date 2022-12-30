from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from collections import defaultdict
from copy import copy


def get_input(file):
    raw = aoc_parse.as_lines(aoc.read_input(2022, 23, file))
    return {c - r * 1j for r, row in enumerate(raw) for c, point in enumerate(row) if point == "#"}


def simulate(elves, rounds=None, until_stationary=None):
    elves = copy(elves)

    # north, south, west, east
    directions = [1j, -1j, -1, 1]

    # for each direction (nswe) check the corresponding three points in space
    # fmt: off
    direction_shifts = {
         1j:[-1,  0, 1 ],
        -1j:[-1,  0, 1 ],
         1 :[-1j, 0, 1j],
        -1 :[-1j, 0, 1j]
    }
    # fmt: on

    # compute directyly the 8 neighbours for complex points
    shifts_1d = [-1, 0, 1]
    complex_neighbours = set(
        complex(dx, dy) for dx in shifts_1d for dy in shifts_1d if dx != 0 or dy != 0
    )

    round = 0
    while until_stationary or (rounds and round < rounds):
        # remember for each destination the elves that tried to go there
        # {position:[list of candidates]}
        candidates = defaultdict(lambda: [])
        for elf in elves:
            # if alone don't move
            if all(elf + step not in elves for step in complex_neighbours):
                continue
            # check first possible direction
            for direction in directions:
                # fmt: off
                if all(elf + direction + shift not in elves for shift in direction_shifts[direction]):
                    # fmt:on
                    # try this new position
                    candidates[elf + direction].append(elf)
                    break

        round += 1

        # check stationarity
        if not candidates and until_stationary:
            return round

        # for each position, if only one elf is trying to move to a place, do it
        for position, elf_queue in candidates.items():
            if len(elf_queue) == 1:
                # remove elf from old position
                elves.remove(elf_queue[0])
                # add elf in new position
                elves.add(position)

        # rotate directions
        directions.append(directions.pop(0))

    xx = {elf.real for elf in elves}
    yy = {elf.imag for elf in elves}
    return int((max(xx) - min(xx) + 1) * (max(yy) - min(yy) + 1) - len(elves))


@aoc.pretty_solution(1)
def part1(data):
    return simulate(data, 10)


@aoc.pretty_solution(2)
def part2(data):
    return simulate(data, until_stationary=True)


def main():
    data = get_input("example2.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 25

    example2 = get_input("example2.txt")
    assert part1(example2) == 110
    assert part2(example2) == 20

    data = get_input("input.txt")
    assert part1(data) == 3970
    assert part2(data) == 923

    print("Test OK")


if __name__ == "__main__":
    test()
    # cProfile.run("main()")
