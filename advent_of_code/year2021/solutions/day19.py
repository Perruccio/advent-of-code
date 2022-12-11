import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse
from numpy import dot, round
from math import sin, cos, pi
from functools import reduce


def round_int(x):
    return int(round(x))


rotations3d = []
tmp = set()
angles = [0, pi / 2, pi, 3 * pi / 2]
for alpha in angles:
    for beta in angles:
        for gamma in angles:
            Rz = [
                [cos(alpha), -sin(alpha), 0],
                [sin(alpha), cos(alpha), 0],
                [0, 0, 1],
            ]
            Ry = [
                [cos(beta), 0, sin(beta)],
                [0, 1, 0],
                [-sin(beta), 0, cos(beta)],
            ]
            Rx = [
                [1, 0, 0],
                [0, cos(gamma), -sin(gamma)],
                [0, sin(gamma), cos(gamma)],
            ]
            R = list(map(lambda v: [round_int(x) for x in v], reduce(dot, [Rz, Ry, Rx])))
            p = tuple(dot(R, [1, 2, 3]))
            if p not in tmp:
                rotations3d.append(R)
                tmp.add(p)


def rotate3d(points):
    res = []
    for R in rotations3d:
        rot_points = []
        for p in points:
            rot_points.append(tuple(dot(R, p)))
        res.append(rot_points)
    return res


def scan(data):
    # choose scanner 0 as reference
    beacons = set(map(tuple, data[0]))
    index_to_visit = list(range(1, len(data)))
    scanners = [(0, 0, 0)]
    while index_to_visit:
        i = index_to_visit.pop(0)
        rotations = rotate3d(data[i])
        match = False
        # check all 24 possible rotations
        for r in rotations:
            # check every possible pair of points if they coincide
            for b1 in beacons:
                for b2 in r:
                    shift = [x2 - x1 for x1, x2 in zip(b1, b2)]
                    shifted = set([tuple(p - s for p, s in zip(point, shift)) for point in r])
                    if len(shifted & beacons) >= 12:
                        beacons |= shifted
                        scanners.append(shift)
                        match = True
                        break
                else:
                    continue
                break
            else:
                continue
            break
        if not match:
            index_to_visit.append(i)

    return beacons, scanners


def part1(beacons):
    return len(beacons)


def part2(scanners):
    max_dist = 0
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            max_dist = max(max_dist, sum([abs(a - b) for a, b in zip(scanners[i], scanners[j])]))
    return max_dist


def main(pretty_print=True):
    raw = aoc_parse.input_as_lines(prj_path + '/year2021/input/day19.txt')

    data = []
    i = 0
    while i < len(raw):
        if 'scanner' in raw[i]:
            scanner, i = [], i + 1
            while i < len(raw) and len(raw[i]) > 0:
                scanner.append(list(map(int, raw[i].split(','))))
                i += 1
            data.append(scanner)
            i += 1

    beacons, scanners = scan(data)

    if pretty_print:
        aoc_output.print_result(1, part1, beacons)
        aoc_output.print_result(2, part2, True, scanners)
    else:
        return part1(beacons), part2(scanners)


if __name__ == "__main__":
    main()
