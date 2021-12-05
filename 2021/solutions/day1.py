import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def part1(v):
    return sum(map(int.__lt__, v, v[1:]))

def part2(v, shift=3):
    return sum(map(int.__lt__, v, v[shift:]))

def main(pretty_print = True):
    
    data = map_input_lines(prj_path + '/input/day1.txt', int)
    
    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)
    
if __name__ == "__main__":
    main()
