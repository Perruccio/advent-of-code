import sys
import pathlib
prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
sys.path.append(prj_path)
from utils.aoc import *

def part1(data):
    def next(i, j, h, w, right):
        next_i = i if right else (i + 1) % h
        next_j = (j + 1) % w if right else j
        return next_i, next_j

    def move(data, h, w, right):
        c = '>' if right else 'v'
        advance = set()
        for i in range(h):
            for j in range(w):
                next_i, next_j = next(i, j, h, w, right)
                if data[i][j] == c and data[next_i][next_j] == '.':
                    advance.add((i, j))
        for (i, j) in advance:
            next_i, next_j = next(i, j, h, w, right)
            data[i][j] = '.'
            data[next_i][next_j] = c
        return data, len(advance) > 0

    h = len(data)
    w = len(data[0])
    i = 0
    while True:
        data, moved_r = move(data, h, w, right=True)
        data, moved_d = move(data, h, w, right=False)
        i += 1
        if not moved_r and not moved_d:
            return i 

def part2():
    return None

def main(pretty_print = True):
    def map_line(line):
        return list(line)

    data = map_input_lines(prj_path + '/year2021/input/day25.txt', map_line )

    if (pretty_print):
        print_result(1, part1, data)
    else:
        return part1(data), part2()

if __name__ == "__main__":
    main()