import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse


def print_points(points):
    h, w = max(p[0] for p in points), max(p[1] for p in points)
    for y in range(w + 1):
        for x in range(h + 1):
            print('██' if (x, y) in points else '  ', end='')
        print()


def fold(points, mirror):
    d, l = mirror
    return {(min(x, 2 * l - x), y) if d == 'x' else (x, min(y, 2 * l - y)) for x, y in points}


def part1(points, foldings):
    return len(fold(points, foldings[0]))


def part2(points, foldings, pretty_print=True):
    for f in foldings:
        points = fold(points, f)
    if (pretty_print):
        print_points(points)
    return len(points)


def main(pretty_print=True):
    raw = aoc_parse.input_as_lines(prj_path + '/year2021/input/day13.txt')
    i = raw.index('')
    points = set(map(lambda s: tuple(map(int, s.split(','))), raw[:i]))
    foldings = list(map(lambda s: (s[0], int(s[1])), map(lambda s: s.split()[-1].split('='), raw[i + 1:])))

    if (pretty_print):
        aoc_output.print_result(1, part1, points, foldings)
        aoc_output.print_result(2, part2, True, points, foldings)
    else:
        return part1(points, foldings), part2(points, foldings, False)


if __name__ == "__main__":
    main()
