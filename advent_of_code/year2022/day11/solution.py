import pathlib
import advent_of_code.utils.aoc as aoc
from collections import deque
import copy
from math import prod
from operator import attrgetter


class Monkey:
    __slots__ = ("items", "operation", "mod", "get_to", "inspected", "cache")
    # lcm common to every monkey
    # warning: this is very bad modeling of lcm and divide_worry...
    lcm = None
    divide_worry = 1

    def __init__(self, items, operation, mod, get_to):
        self.items = items
        self.operation = operation
        self.mod = mod
        self.get_to = get_to
        self.inspected = 0
        self.cache = {}  # old:new, to

    @classmethod
    def create_monkey(cls, lines):
        # NB assuming a lot about the structure of lines data
        assert len(lines) == 6
        items = deque(aoc.get_ints(lines[1]))
        # hacky solution with eval. one should parse the operation
        operation = eval("lambda old : " + lines[2].split("=")[1])
        mod = aoc.get_ints(lines[3])[0]
        to_if_true = aoc.get_ints(lines[4])[0]
        to_if_false = aoc.get_ints(lines[5])[0]
        return cls(items, operation, mod, lambda x: [to_if_false, to_if_true][x % mod == 0])

    def throw(self):
        # take items from left
        old = self.items.popleft()
        self.inspected += 1
        if old not in self.cache:
            # compute new worry level
            new = self.operation(old) // Monkey.divide_worry
            if Monkey.lcm:
                new %= Monkey.lcm
            self.cache[old] = (new, self.get_to(new))
        return self.cache[old]

    def catch(self, item):
        self.items.append(item)


def get_input(file):
    raw = aoc.input_as_string(str(pathlib.Path(__file__).parent) + "/" + file)
    # split in \n\n to get each raw monkey, then split in \n to get lines
    return [Monkey.create_monkey(raw_monkey.split("\n")) for raw_monkey in raw.split("\n\n")]


def solve(monkeys, rounds):
    for _ in range(rounds):
        for monkey in monkeys:
            # use all items for each monkey
            while monkey.items:
                item, to = monkey.throw()
                monkeys[to].catch(item)
    # compute 2 greatest inspections and multiply
    insp1, insp2 = sorted(map(attrgetter("inspected"), monkeys), reverse=True)[:2]
    return insp1 * insp2


@aoc.pretty_solution(1)
def part1(monkeys, rounds=20):
    # NB avoid modifying monkeys, so that part 2 will begin from original state
    monkeys = copy.deepcopy(monkeys)
    Monkey.divide_worry = 3
    return solve(monkeys, rounds)


@aoc.pretty_solution(2)
def part2(monkeys, rounds=10000):
    # not really a lcm
    Monkey.lcm = prod(monkey.mod for monkey in monkeys)
    Monkey.divide_worry = 1
    return solve(monkeys, rounds)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 10605
    assert part2(example) == 2713310158

    data = get_input("input.txt")
    assert part1(data) == 61005
    assert part2(data) == 20567144694

    print("Test OK")


if __name__ == "__main__":
    test()
