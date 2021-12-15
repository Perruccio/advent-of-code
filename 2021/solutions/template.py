import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def part1(data):
    pass

def part2(data):
    pass

def main(pretty_print = True):
    def map_line(line):
        pass
    
    data = map_input_lines(prj_path + '/input/day.txt', map_line)
    
    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)
   
if __name__ == "__main__":
    main()