import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *
from collections import defaultdict

def straight(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return x1 == x2 or y1 == y2

def diag(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return abs(x2 - x1) == abs(y2 - y1)

def move(point, dir):
    return (point[0] + dir[0], point[1] + dir[1])

def get_overlaps(data, can_overlap):
    overlaps = defaultdict(int)
    for vertices in data:
        if can_overlap(vertices):
            (x1, y1), (x2, y2) = vertices[0], vertices[1]
            # compute directions (without step size)
            x_dir, y_dir = sign(x2 - x1), sign(y2 - y1)
            n_steps = max(abs(x2 - x1), abs(y2 - y1))
            # add visited steps
            for i in range(0, n_steps + 1):
                overlaps[move(vertices[0], (i * x_dir, i * y_dir))] += 1
                
    return sum(1 for value in overlaps.values() if value > 1)

def part1(data):
    return get_overlaps(data, lambda v: straight(*v))
            
def part2(data):
    return get_overlaps(data, lambda v: straight(*v) or diag(*v))

def main(pretty_print = True):
    def process_line(line):
        (x1, y1), (x2, y2) = map(lambda s: map(int, s.split(',')), line.split('->'))
        return (x1, y1), (x2, y2)
    
    data = map_input_lines(prj_path + '/input/day05.txt', process_line)
    
    if (pretty_print):
        print_results(1, part1, data)
        print_results(2, part2, data)
    else:
        return part1(data), part2(data)
   
if __name__ == "__main__":
    main()