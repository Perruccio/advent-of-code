import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def part1(data):
    horizontal = sum(x[1] for x in data if x[0] == 'forward')
    depth = sum(
        -x[1] if x[0] == 'up' else
        x[1] if x[0] == 'down' else
        0
        for x in data)
    return horizontal * depth

def part2(data):
    h_pos = 0
    d_pos = 0
    aim = 0
    for dir, step in data:
        if dir == "down":
            aim += step
        elif dir == "up":
            aim -= step
        elif dir == "forward":
            h_pos += step
            d_pos += aim*step
    return h_pos * d_pos

def main(pretty_print = True):

    def map_line(line):
        a, b = line.split()
        return a, int(b)

    data = map_input_lines(prj_path + '/year_2021/input/day02.txt', map_line)

    if (pretty_print):
        print_result(1, part1, data)
        print_result(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()
