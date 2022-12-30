import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def population(init_state, time):
    # use counter, state_count[i] = num of fish with i days to procreate
    state_count = [init_state.count(i) for i in range(0, 9)]
    for _ in range(0, time):
        # rotate list (diminuish day counter of each fish by 1)
        # this also adds newborn fish
        state_count.append(state_count[0])
        s0 = state_count.pop(0)
        # reset counter of fish that gave birth to 6
        state_count[6] += s0
    return sum(state_count)


@aoc.pretty_solution(1)
def part1(data):
    return population(data, 80)


@aoc.pretty_solution(2)
def part2(data):
    return population(data, 256)


def main():
    data = list(map(int, aoc_parse.input_as_string(prj_path + '/year2021/input/day06.txt').split(',')))
    return part1(data), part2(data)


if __name__ == "__main__":
    main()
