import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.utils import output as aoc_output, parse as aoc_parse


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


def part1(data):
    return population(data, 80)


def part2(data):
    return population(data, 256)


def main(pretty_print=True):
    data = list(map(int, aoc_parse.input_as_string(prj_path + '/year2021/input/day06.txt').split(',')))

    if pretty_print:
        aoc_output.print_result(1, part1, data)
        aoc_output.print_result(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main()
