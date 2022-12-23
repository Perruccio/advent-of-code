import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse


def get_input(file):
    raw =  aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    return {c - r*1j for r, row in enumerate(raw) for c, point in enumerate(row) if point == "#"}

def complex_neighbours(x):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                yield complex(x.real + dx, x.imag + dy)

def simulate(elves, rounds, until_still):
    directions = [1j, -1j, -1, 1]

    direction_shifts = {
         1j:[-1,  0, 1 ],
        -1j:[-1,  0, 1 ],
         1 :[-1j, 0, 1j],
        -1 :[-1j, 0, 1j]
    }

    round = 0
    while round < rounds or until_still:
        # NB {destination:elf}
        new_elves = {}
        still = set()
        for elf in elves:
            # if alone don't move
            if all(neigh not in elves for neigh in complex_neighbours(elf)):
                new_elves[elf] = elf
                still.add(elf)
                continue
            # check first possible direction
            for direction in directions:
                if all(elf + direction + shift not in elves for shift in direction_shifts[direction]):
                    try_pos = elf + direction
                    if try_pos not in new_elves:
                        new_elves[try_pos] = elf
                    else:
                        new_elves[elf] = elf
                        new_elves[new_elves[try_pos]] = new_elves[try_pos]
                        new_elves[try_pos] = None
                    break
            else:
                new_elves[elf] = elf
        
        round += 1
        if until_still and len(still) == len(elves):
            return round
        elves = set(elf for elf, pos in new_elves.items() if pos is not None)
        directions = directions[1:] + [directions[0]]
    min_x, max_x = int(min(elf.real for elf in elves)), int(max(elf.real for elf in elves))
    min_y, max_y = int(min(elf.imag for elf in elves)), int(max(elf.imag for elf in elves))
    universe = {x + 1j*y for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)}
    return len(universe - elves)

@aoc_output.pretty_solution(1)
def part1(data):
    return simulate(data, 10, False)

@aoc_output.pretty_solution(2)
def part2(data):
    return simulate(data, 0, True)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 110
    assert part2(example) == 20

    data = get_input("input.txt")
    assert part1(data) == 3970
    assert part2(data) == 923

    print("Test OK")


if __name__ == "__main__":
    test()
