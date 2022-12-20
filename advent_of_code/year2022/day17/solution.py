from collections import defaultdict
import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse


def get_input(file):
    return aoc_parse.input_as_string(str(pathlib.Path(__file__).parent) + "/" + file)


def spawn_rock(rock_type, height, pad_left):
    match rock_type:
        case "-":
            rock = set(pad_left + x + height * 1j for x in range(4))
        case "+":
            rock = set(pad_left + x + (height + 1) * 1j for x in range(3))
            rock.update(pad_left + 1 + (height + y) * 1j for y in range(3))
        case "L":
            # NB mirror L
            rock = set(pad_left + x + height * 1j for x in range(3))
            rock.update(pad_left + 2 + (height + y) * 1j for y in range(3))
        case "I":
            rock = set(pad_left + (height + y) * 1j for y in range(4))
        case "square":
            rock = set(pad_left + x + height * 1j for x in range(2))
            rock.update(pad_left + x + (height + 1) * 1j for x in range(2))
        case _:
            raise "Rock type"
    return rock


def simulate_rock(rock, data, i, solid, limits):
    while True:
        # move rock: first push then fall
        new_rock = set(point + data[i] for point in rock)
        # check if moved rock collides with something (wall or other rocks)
        if not (new_rock & solid) and all(limits[0] <= point.real <= limits[1] for point in new_rock):
            rock = new_rock

        # advance and loop i
        i = (i + 1) % len(data)

        # fall
        new_rock = set(point - 1j for point in rock)
        # check if rock stops (intersect with solid after fall)
        if solid & new_rock:
            break
        rock = new_rock
    return rock, i


def simulate_tetris(data, max_rocks):
    # known data
    rock_types = ["-", "+", "L", "I", "square"]
    floor = 0
    data = [-1 if jet == "<" else 1 for jet in data]
    # left, right limits
    limits = 0, 6
    # initialization to start position
    n_rocks = 0
    rock_type = 0
    height = floor
    # add flor to solid
    solid = set(range(limits[0], limits[1] + 1))
    i = 0  # i is data's index (data[i] = -1 or +1)
    # store index when rock_type = 0 to identify cycles
    i_with_rock_0 = {}
    # {n_rocks:height}
    heights = {0: floor}
    while n_rocks < max_rocks:
        # rock types are over, store index to identify cycles
        if rock_type == 0:
            if i not in i_with_rock_0:
                # go on
                i_with_rock_0[i] = height, n_rocks
            else:
                # cycle is identified (i already visited with rock_type = 0)
                # is this actually a particular case?

                # get height and n_rocks when we visited this index i with rock_type 0.
                # this is becase we're going to add last height + cycle_height * n_cycle + remaining
                # as (last height + remaining) + cycle_height * n_cycle. this is useful because "remaining"
                # follows last height (cycle is a multiple of len(last_n_rocks))
                last_height, last_n_rocks = i_with_rock_0[i]
                # rocks in cycle is n_rocks now (before new cycle start) - rocks before this cycle started
                rocks_in_cycle = n_rocks - last_n_rocks
                # (height of a cycle) * (number of cycles)
                cycles_height = (height - last_height) * (max_rocks // rocks_in_cycle)
                # remaining includes rocks before first cycle and rocks after last cycle
                # basically removing all cycles from max_rocks
                remaining = heights[max_rocks % rocks_in_cycle]
                return remaining + cycles_height

        # main part
        # spawn new rock
        rock = spawn_rock(rock_types[rock_type], height + 4, pad_left=2)
        rock_type = (rock_type + 1) % len(rock_types)

        # push left/right and let fall until stops
        rock, i = simulate_rock(rock, data, i, solid, limits)

        # update state
        n_rocks += 1
        solid |= rock
        height = int(max(height, max(point.imag for point in rock)))

        # store also heights depending on number of rocks for correcly computing height with cycles
        heights[n_rocks] = height

    return height


@aoc_output.pretty_solution(1)
def part1(data):
    return simulate_tetris(data, 2022)


@aoc_output.pretty_solution(2)
def part2(data):
    return simulate_tetris(data, 1_000_000_000_000)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 3068
    assert part2(example) == 1514285714288

    data = get_input("input.txt")
    assert part1(data) == 3149
    assert part2(data) == 1553982300884

    print("Test OK")


if __name__ == "__main__":
    test()
