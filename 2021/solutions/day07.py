import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from statistics import median

def part1(data):
    # problem is min_m \sum_i |m - x_i|
    # set d (\sum_i |m - x_i|) / dm = 0
    # \sum_i sgn(m - x_i) = 0 <=> m = median(x)
    m = round(median(data))
    return sum([abs(x - m) for x in data])

def part2(data):
    # problem is min_m \sum_i |m - x_i|(|m - x_i| + 1) / 2
    # (we used sum_{i = 0}^n = n(n+1)/2)
    # set d(...) / dm = 0
    # by standard manipulation we find m = mean(x) - 1/2 * sum_i sgn(x_i - m) / n
    # (where n = len(x))
    # hence mean(x) - 1/2 <= m <= mean(x) + 1/2
    m1 = sum(data) // len(data) # floor(mean)
    def fuel(m):
        return sum([abs(x - m)*(abs(x - m) + 1) for x in data]) // 2
    return min(fuel(m1), fuel(m1 + 1))

def main(pretty_print = True):

    data = list(map(int, input_as_string(prj_path + '/input/day07.txt').rstrip().split(',')))

    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)

if __name__ == "__main__":
    main()