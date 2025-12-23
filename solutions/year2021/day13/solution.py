import pathlib
import aoc.parse
import aoc


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
    raw = aoc.parse.input_as_lines(str(pathlib.Path(__file__).parent/'input.txt'))
    i = raw.index('')
    points = set(map(lambda s: tuple(map(int, s.split(','))), raw[:i]))
    foldings = list(map(lambda s: (s[0], int(s[1])), map(lambda s: s.split()[-1].split('='), raw[i + 1:])))
    return part1(points, foldings), part2(points, foldings)
    

def test():
    p1, p2 = main()
    assert p1 == 788
    assert p2 == 102


if __name__ == "__main__":
    main()
