import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse
from statistics import median


def is_open(p):
    return p in ['(', '[', '{', '<']


def match(o, c):
    return c == {'(': ')', '[': ']', '{': '}', '<': '>'}[o]


def part1(data):
    points = {')': 3, ']': 57, '}': 1197, '>': 25137}
    score = 0
    for line in data:
        stack = []
        for p in line:
            if is_open(p):
                stack.append(p)
            elif not match(stack.pop(), p):
                score += points[p]
                break
    return score


def part2(data):
    def compute_score(line):
        points = {'(': 1, '[': 2, '{': 3, '<': 4}
        score = 0
        for i in range(len(line) - 1, -1, -1):
            score = score * 5 + points[line[i]]
        return score

    scores = []
    for line in data:
        stack = []
        for p in line:
            if is_open(p):
                stack.append(p)
            elif not match(stack.pop(), p):
                stack = []
                break
        if stack:
            scores.append(compute_score(stack))
    return median(scores)


def main(pretty_print=True):
    def map_line(line):
        return line

    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day10.txt', map_line)

    if pretty_print:
        aoc_output.print_result(1, part1, data)
        aoc_output.print_result(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main()
