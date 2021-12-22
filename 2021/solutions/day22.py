import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
import re

def solve(data, ignore=lambda _:False):
    def check(olds, new, new_cuboids):
        for c in olds:
            intersection = c.intersection(new, -c.on)
            if intersection is not None:
                new_cuboids.add(intersection)
        return new_cuboids

    intersections = set()
    originals = set()
    for step in data:
        cuboid = Cuboid(*step[1:], step[0])
        if ignore(cuboid):
            continue
        new_cuboids = check(originals, cuboid, set())
        if new_cuboids:
            new_cuboids = check(intersections, cuboid, new_cuboids)

        originals.add(cuboid)
        intersections |= new_cuboids
    return sum([c.on * c.volume() for c in originals | intersections])

def part1(data):
    return solve(data, lambda c: not c.is_small())

def part2(data):
    return solve(data)

def main(pretty_print = True):
    def map_line(line):
        on, data = line.split(' ')
        on = int(on == 'on')
        data = re.findall(RE['int'], data)
        return on, (int(data[0]), int(data[1])), (int(data[2]), int(data[3])), (int(data[4]), int(data[5]))

    data = map_input_lines(prj_path + '/input/day22.txt', map_line)

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()