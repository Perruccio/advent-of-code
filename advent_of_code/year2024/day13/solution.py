from advent_of_code.lib.all import *

class Machine():
    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize


def get_input(file):
    raw = aoc.read_input(2024, 13, file)
    lines = aoc_parse.as_lines(raw)
    machines = []
    for i in range(0, len(lines), 4):
        a, b, prize = map(aoc_parse.get_ints, (lines[i], lines[i+1], lines[i+2]))
        machines.append(Machine(a, b, prize))
    return machines


def solve(data, prize_shift = 0):
    a_cost, b_cost = 3, 1
    res = 0
    for machine in data:
        (xa, ya), (xb, yb), (x, y) = machine.a, machine.b, machine.prize
        x, y = x + prize_shift, y + prize_shift
        # solve the linear 2x2 system to find the solution IF unique.
        # ignore case det == 0 (ok if impossible, one could solve the diophantine equation if undetermined)
        det = xa*yb - xb*ya
        if det == 0:
            continue
        na, rem_a = divmod(yb*x - xb*y, det)
        nb, rem_b = divmod(-ya*x + xa*y, det)
        if rem_a == rem_b == 0:
            res += na*a_cost + nb*b_cost
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, 10000000000000)


def test():
    data = get_input("input.txt")
    assert part1(data) == 39748 	
    assert part2(data) == 74478585072604 	
    print("Test OK")


if __name__ == "__main__":
    test()
