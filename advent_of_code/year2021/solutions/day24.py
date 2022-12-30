import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_info(data):
    dd, cc, oo = [], [], []
    for i in range(0, len(data), len(data) // 14):
        dd.append(data[i + 4][1][1])
        cc.append(data[i + 5][1][1])
        oo.append(data[i + 15][1][1])
    return dd, cc, oo


def solve(dd, cc, oo, max_model):
    model = [0] * 14
    z = []
    for i in range(len(model)):
        if dd[i] == 1:
            z.append(i)
        else:
            last_i = z.pop()
            delta = oo[last_i] + cc[i]
            model[last_i] = min(9, 9 - delta) if max_model else max(1, 1 - delta)
            model[i] = model[last_i] + delta
    return sum([model[len(model) - i - 1] * 10 ** i for i in range(len(model))])


@aoc.pretty_solution(1)
def part1(dd, cc, oo):
    return solve(dd, cc, oo, True)


@aoc.pretty_solution(2)
def part2(dd, cc, oo):
    return solve(dd, cc, oo, False)


def main():
    def map_line(line):
        l = line.split()
        return l[0], tuple([int(x) if x[0] == '-' or x.isnumeric() else x for x in l[1:]])

    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day24.txt', map_line)
    dd, cc, oo = get_info(data)
    return part1(dd, cc, oo), part2(dd, cc, oo)


if __name__ == "__main__":
    main()
