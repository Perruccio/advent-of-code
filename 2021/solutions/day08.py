import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def pattern_to_digit(patterns):
    # pattern : digit
    p2d = {}
    # first find digit with unique number of segments
    for p in patterns:
        l = len(p)
        if l == 2:
            p2d[p] = 1
        elif l == 3:
            p2d[p] = 7
        elif l == 4:
            p2d[p] = 4
        elif l == 7:
            p2d[p] = 8

    # digit : pattern
    d2p = {v: k for k, v in p2d.items()}

    # find digit without unique n of segments
    # by exploiting previous information
    for p in patterns:
        l = len(p)
        if l == 5:
            # d = 2, 3 or 5
            if set(d2p[1]).issubset(p):
                p2d[p] = 3
            elif len(set(d2p[4]).difference(p)) == 1:
                p2d[p] = 5
            else:
                p2d[p] = 2
        elif l == 6:
            # d = 0, 6, 9
            if len(set(d2p[1]).difference(p)) == 1:
                p2d[p] = 6
            elif len(set(d2p[4]).difference(p)) == 0:
                p2d[p] = 9
            else:
                p2d[p] = 0
    return p2d

def part1(data):
    def check(n):
        return n == 1 or n == 4 or n == 7 or n == 8

    res = 0
    for line in data:
        p2d = pattern_to_digit(line[0])
        res += sum([check(p2d[x]) for x in line[1]])
    return res

def part2(data):
    res = 0
    for line in data:
        p2d = pattern_to_digit(line[0])
        res += sum([10**i * p2d[line[1][3 - i]] for i in range(4)])
    return res

def main(pretty_print = True):

    # use frozen set as keys of dict (standard sets are not hashable)
    def map_line(line):
        a, b = line.split('|')
        return list(map(frozenset, a.split())), list(map(frozenset, b.split()))

    data = map_input_lines(prj_path + '/input/day08.txt', map_line)

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()
