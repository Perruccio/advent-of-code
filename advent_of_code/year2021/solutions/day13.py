import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def print_points(points):
    h, w = max(p[0] for p in points), max(p[1] for p in points)
    for y in range(w + 1):
        for x in range(h + 1):
            print('* ' if (x, y) in points else '  ', end='')
        print()


def fold(points, mirror):
    d, l = mirror
    return {(min(x, 2 * l - x), y) if d == 'x' else (x, min(y, 2 * l - y)) for x, y in points}


@aoc.pretty_solution(1)
def part1(points, foldings):
    return len(fold(points, foldings[0]))


@aoc.pretty_solution(2)
def part2(points, foldings, ):
    for f in foldings:
        points = fold(points, f)
    print_points(points)
    return len(points)


def main():
    raw = aoc_parse.input_as_lines(prj_path + '/year2021/input/day13.txt')
    i = raw.index('')
    points = set(map(lambda s: tuple(map(int, s.split(','))), raw[:i]))
    foldings = list(map(lambda s: (s[0], int(s[1])), map(lambda s: s.split()[-1].split('='), raw[i + 1:])))
    return part1(points, foldings), part2(points, foldings)


if __name__ == "__main__":
    main()
