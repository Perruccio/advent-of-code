import pathlib
import aoc.parse
import aoc
import aoc.geometry as aoc_geometry
import re


def solve(data):
    def untouched_volume(cuboid, next):
        """ return only the volume of cuboid that
        will never be changed by following instructions"""
        intersections = [cuboid.intersect(c) for c in next if cuboid.intersect(c)]
        return cuboid.volume() - sum(
            [untouched_volume(intersections[i], intersections[i + 1:]) for i in range(len(intersections))])

    # read the data
    ons, cuboids = zip(*map(lambda step: (step[0], aoc_geometry.Cuboid(*step[1:])), data))
    # for each cuboid, add up only the part of the volume that will never change
    return sum([untouched_volume(cuboids[i], cuboids[i + 1:]) for i in range(len(ons)) if ons[i] == 1])


@aoc.pretty_solution(1)
def part1(data):
    data = [l for l in data if aoc_geometry.Cuboid(*l[1:]).is_small(50)]
    return solve(data)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data)


def main():
    def map_line(line):
        on, data = line.split(' ')
        on = int(on == 'on')
        data = re.findall(aoc.parse.RE['int'], data)
        return on, (int(data[0]), int(data[1])), (int(data[2]), int(data[3])), (int(data[4]), int(data[5]))

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 580098
    assert p2 == 1134725012490723


if __name__ == "__main__":
    main()
