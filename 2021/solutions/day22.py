import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
import re

def intersect1d(aa, bb):
    l = max(aa[0], bb[0])
    r = min(aa[1], bb[1])
    return (l, r) if l <= r else None

class Cuboid():
    def __init__(self, xx, yy, zz, on=1):
        assert xx[0] <= xx[1] and yy[0] <= yy[1] and zz[0] <= zz[1]
        self.xx = xx
        self.yy = yy
        self.zz = zz
        self.on = on

    def is_small(self):
        return all(-50 <= tt[0] and tt[1] <= 50 for tt in [self.xx, self.yy, self.zz])

    def size(self):
        return (self.xx[1] - self.xx[0] + 1) * (self.yy[1] - self.yy[0] + 1) * (self.zz[1] - self.zz[0] + 1)

    def intersection(self, other, on):
        xx = intersect1d(self.xx, other.xx)
        yy = intersect1d(self.yy, other.yy)
        zz = intersect1d(self.zz, other.zz)
        if any([t is None for t in [xx, yy, zz]]):
            return None
        return Cuboid(xx, yy, zz, on)

def solve(data, part1=False):
    visited = set()
    for step in data:
        cuboid = Cuboid(*step[1:], step[0])
        if part1 and not cuboid.is_small():
            continue
        new_cuboids = set([cuboid]) if cuboid.on else set()
        for c in visited:
            intersection = c.intersection(cuboid, -c.on)
            if intersection is not None:
                new_cuboids.add(intersection)
        visited |= new_cuboids
    print(len(visited))
    return sum([c.on * c.size() for c in visited])

def part1(data):
    return solve(data, True)

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