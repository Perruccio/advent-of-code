import pathlib
import aoc.parse
import aoc
from statistics import median


def is_open(p):
    return p in ['(', '[', '{', '<']


def match(o, c):
    return c == {'(': ')', '[': ']', '{': '}', '<': '>'}[o]


@aoc.pretty_solution(1)
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


@aoc.pretty_solution(2)
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


def main():
    def map_line(line):
        return line

    data = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 411471
    assert p2 == 3122628974


if __name__ == "__main__":
    main()
