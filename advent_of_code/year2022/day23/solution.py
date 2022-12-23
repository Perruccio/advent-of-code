import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from copy import copy
import cProfile


def get_input(file):
    raw = aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    return {c - r * 1j for r, row in enumerate(raw) for c, point in enumerate(row) if point == "#"}


def complex_neighbours(x):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                yield complex(x.real + dx, x.imag + dy)


def simulate(elves, rounds=None, until_stationary=None):
    directions = [1j, -1j, -1, 1]
    # fmt: off
    direction_shifts = {
         1j:[-1,  0, 1 ],
        -1j:[-1,  0, 1 ],
         1 :[-1j, 0, 1j],
        -1 :[-1j, 0, 1j]
    }
    # fmt: on

    round = 0
    while until_stationary or (rounds and round < rounds):
        # remember for each destination the elf that tried to go there
        try_positions = {}
        new_elves = copy(elves)
        for elf in elves:
            # if alone don't move, already included in new_elves
            if all(neigh not in elves for neigh in complex_neighbours(elf)):
                continue
            # check first possible direction
            for direction in directions:
                if all(elf + direction + shift not in elves for shift in direction_shifts[direction]):
                    # try this new position
                    try_pos = elf + direction
                    if try_pos not in try_positions:
                        try_positions[try_pos] = elf
                        new_elves.remove(elf)
                    else:
                        # another elf tried to go there. both elves return to original position
                        new_elves.add(try_positions[try_pos])
                        try_positions[try_pos] = None
                    break

        round += 1
        if until_stationary and len(elves) == len(new_elves):
            return round

        elves = new_elves
        elves.update(elf for elf, old_elf in try_positions.items() if old_elf is not None)
        directions = directions[1:] + [directions[0]]

    min_x, max_x = int(min(elf.real for elf in elves)), int(max(elf.real for elf in elves))
    min_y, max_y = int(min(elf.imag for elf in elves)), int(max(elf.imag for elf in elves))
    universe = {x + 1j * y for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)}
    return len(universe - elves)


@aoc_output.pretty_solution(1)
def part1(data):
    return simulate(data, 10)


@aoc_output.pretty_solution(2)
def part2(data):
    return simulate(data, until_stationary=True)


def main():
    data = get_input("input.txt")
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
    main()
    # cProfile.run("main()")
