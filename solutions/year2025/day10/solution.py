from aoc.all import *
from scipy.optimize import linprog


def get_input(file):
    raw = aoc.read_input(2025, 10, file)
    data = []
    for line in raw.splitlines():
        machine, *buttons, joltage = line.split(" ")
        machine = [1 if x == "#" else 0 for x in machine[1:-1]]
        buttons = list(tuple(map(int, button[1:-1].split(","))) for button in buttons)
        joltage = list(map(int, joltage[1:-1].split(",")))
        data.append((machine, buttons, joltage))
    return data


@aoc.pretty_solution(1)
def part1(data):
    def solve(machine, buttons):
        if sum(machine) == 0:
            return 0

        res = 1e9
        # each button can either be pressed exactly once or 0.
        # 2+ times are useless.
        # NB at each iteration, we compute only the value when i-th 
        # button is pressed and it's the first to be pressed
        for i, button in enumerate(buttons):
            machine_copy = copy(machine)
            for b in button:
                machine_copy[b] = 1 - machine_copy[b]
            # NB we just need buttons[i+1:], check only the case
            # where i-th button is the first (for each i)
            res = min(res, 1 + solve(machine_copy, buttons[i+1:]))
        return res
    
    return sum(solve(machine, buttons) for machine, buttons, _ in data)


@aoc.pretty_solution(2)
def part2(data):
    # each button is a vector of zero and ones (1 values are
    # in the positions given by the button tuple
    # e.g. button = (1, 4) -> vector = [0, 1, 0, 0, 1] (column)
    # then the problem is equivalent to putting every button vector
    # in a matrix A and solve A*x = jolt, with x having least l1 norm.
    # i.e.
    # min_x dot(c, x) (c = [1, 1, ... , 1])
    # s.t.  - A*x = b
    #       - x >= 0
    #       - x integer
    # we use scipy.linprog
    res = 0
    for _, buttons, machine in data:
        A = [[0]*len(buttons) for _ in range(len(machine))]
        for c, button in enumerate(buttons):
            for b in button:
                A[b][c] = 1
        x = linprog([1]*len(buttons), A_eq=A, b_eq=machine, bounds=(0, None), integrality=1).x
        res += round(sum(x))
    return res


def main():
    data = get_input("input.txt")
    part1(deepcopy(data))
    part2(deepcopy(data))


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 425
    assert part2(deepcopy(data)) == 15883
    print("Test OK")


if __name__ == "__main__":
    main()
