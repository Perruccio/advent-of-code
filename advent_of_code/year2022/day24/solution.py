import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from advent_of_code.utils import math as aoc_math
from collections import deque
from math import lcm
from copy import deepcopy


def get_input(file):
    raw = aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    # directions map in complex plane. NB up is -1j
    directions = {">": 1, "<": -1, "^": -1j, "v": 1j}

    # blizzards is a list of [position, direction] so that different blizzards can occupy
    # the same position and position can be modified with time
    blizzards = dict()
    for r, line in enumerate(raw[1:]):
        for c, point in enumerate(line[1:]):
            if point in directions:
                blizzards[complex(c, r)] = directions[point]
    return blizzards, len(raw[0])-2, len(raw)-2


def simulate(data, come_back=False):
    # get problem data
    blizzards, width, height = deepcopy(data)
    start, end = -1j, width - 1 + height * 1j
    # init
    # t is time, blocked = {time:blocked positions}
    t, seen = 0, set()
    # mod_space will be used to wrap around blizzards
    mod_space = width + 1j * height
    # mod_time is used to capture cycle in blizzard movements
    mod_time = lcm(width, height)
    # bfs
    todo = deque([(start, t)])
    goals = [end, start, end] if come_back else [end]
    while goals:
        pos, t = todo.popleft()

        # check if over or go back
        if pos == goals[0]:
            goals.pop(0)
            seen = set()
            todo = deque([(pos, t)])
            continue

        t += 1
        t_mod = t % mod_time

        # consider all possible moves
        for move in [1, 1j, 0, -1, -1j]:
            new_pos = pos + move

            # check if in boundaries
            if new_pos != start and new_pos != end and not (0 <= new_pos.real < width and 0 <= new_pos.imag < height):
                continue

            # check if space is free
            for move in [1, 1j, -1, -1j]:
                origin = aoc_math.complex_modulo(new_pos - move * t, mod_space)
                if origin in blizzards and blizzards[origin] == move:
                    break
            else:
                if (new_pos, t_mod) not in seen:
                    seen.add((new_pos, t_mod))
                    todo.append((new_pos, t))
    return t

@aoc_output.pretty_solution(1)
def part1(data):
    return simulate(data)


@aoc_output.pretty_solution(2)
def part2(data):
    return simulate(data, come_back=True)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 18
    # assert part2(example) == 54

    # data = get_input("input.txt")
    # assert part1(data) == 228
    # assert part2(data) == 723

    print("Test OK")


if __name__ == "__main__":
    test()
