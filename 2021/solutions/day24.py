import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def get_info(data):
    dd, cc, oo = [], [], []
    for i in range(0, len(data), len(data) // 14):
        dd.append(data[i+4][1][1])
        cc.append(data[i+5][1][1])
        oo.append(data[i+15][1][1])
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

def part1(dd, cc, oo):
    return solve(dd, cc, oo, True)

def part2(dd, cc, oo):
    return solve(dd, cc, oo, False)

def main(pretty_print = True):
    def map_line(line):
        l = line.split()
        return (l[0], tuple([int(x) if x[0] == '-' or x.isnumeric() else x for x in l[1:]]))

    data = map_input_lines(prj_path + '/input/day24.txt', map_line)
    dd, cc, oo = get_info(data)

    if (pretty_print):
        print_results(1, part1, dd, cc, oo)
        print_results(2, part2, dd, cc, oo)
    else:
        return part1(dd, cc, oo), part2(dd, cc, oo)

if __name__ == "__main__":
    main()