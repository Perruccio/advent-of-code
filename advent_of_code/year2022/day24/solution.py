import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse
from collections import deque
from copy import deepcopy

def get_input(file):
    raw = aoc_parse.input_as_lines(str(pathlib.Path(__file__).parent) + "/" + file)
    # directions map in complex plane. NB up is -1j
    directions = {">": 1, "<": -1, "^": -1j, "v": 1j}
    blizzards, walls = {}, set()
    i = 0
    for r, line in enumerate(raw):
        for c, point in enumerate(line):
            if point == "#":
                walls.add(complex(c, r))
            elif point in directions:
                blizzards[i] = [complex(c, r), directions[point]]
                i += 1
    return blizzards, walls, len(raw[0]), len(raw)


def complex_modulo(x, mod):
    return (x.real % mod.real) + 1j * (x.imag % mod.imag)


def get_blocked(blizzards):
    return set(blizz[0] for blizz in blizzards.values())


def make_move(t, pos, direction, blocked, walls, todo, visited):
    new_pos = pos + direction
    if (new_pos, t) not in visited and new_pos not in blocked and new_pos not in walls:
        todo.append((new_pos, t))
        visited.add((new_pos, t))
        return True
    return False


def print_blocked(t, blocked):
    print(f"{t=}")
    aoc_output.print_grid_from_complex({b: 1 for b in blocked})
    print()

def simulate(data, come_back=False):
    blizzards, walls, width, height = deepcopy(data)
    start = 1
    end = width - 2 + (height - 1) * 1j
    walls.add(start - 1j)
    walls.add(end + 1j)
    t = 0
    todo = deque([(start, 0)])
    blocked = {0: get_blocked(blizzards)}
    mod = width + 1j * height
    visited = set()
    done = 0
    while todo:
        pos, t = todo.popleft()

        if pos == end:
            done += 1
            if done == 3 or not come_back:
                return t
            visited = set()
            start, end = end, start
            todo = deque([(start, t)])
            continue

        t += 1

        # move all blizzards
        if t not in blocked:
            for blizz in blizzards.values():
                blizz[0] += blizz[1]
                if blizz[0] in walls:
                    blizz[0] = complex_modulo(blizz[0] + 2 * blizz[1], mod)
            blocked[t] = get_blocked(blizzards)

        # greedy
        for move in [1, 1j, 0, -1, -1j]:
            make_move(t, pos, move, blocked[t], walls, todo, visited)


@aoc_output.pretty_solution(1)
def part1(data):
    return simulate(data)

@aoc_output.pretty_solution(2)
def part2(data):
    return simulate(data, come_back = True)


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
