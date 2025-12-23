import aoc.parse
from aoc import aoc
from copy import copy


def get_input(file):
    raw = aoc.parse.as_lines(aoc.read_input(2022, 23, file))
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
        # compute new set of elves.
        new_elves = copy(elves)
        for elf in elves:
            # if alone don't move
            if all(elf + step not in elves for step in complex_neighbours):
                continue
            # check first possible direction
            for direction in directions:
                # fmt: off
                if all(elf + direction + shift not in elves for shift in direction_shifts[direction]):
                    # fmt:on
                    # move if nobody has already tried to move there
                    if (new_elf := elf + direction) not in new_elves:
                        new_elves.remove(elf)
                        new_elves.add(new_elf)
                    else:
                        # only possible collision is from opposite elves!
                        # just replace both at original positions
                        new_elves.add(elf)
                        new_elves.remove(new_elf)
                        new_elves.add(elf + 2*direction)
                    break
        round += 1

        # check stationarity
        if new_elves == elves and until_stationary:
            return round

        elves = new_elves

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
