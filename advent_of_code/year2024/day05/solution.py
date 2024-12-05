from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 5, file)
    order_raw, updates = raw.split("\n\n")
    order = defaultdict(set)
    for line in order_raw.split("\n"):
        a, b = line.split("|")
        order[int(a)].add(int(b))
    updates = [list(map(int, update.split(","))) for update in updates.split("\n")]
    return order, updates


def is_sorted_pair(order, a, b):
    # not transitive!! just check directly
    return b in order[a]

def is_sorted_vector(order, v):
    return all(is_sorted_pair(order, a, b) for a, b in zip(v, v[1:]))


@aoc.pretty_solution(1)
def part1(order, updates):
    return sum(v[len(v)//2] for v in updates if is_sorted_vector(order, v))


@aoc.pretty_solution(2)
def part2(order, updates):
    res = 0
    for update in updates:
        if is_sorted_vector(order, update):
            continue
        # bubble sort: don't rely on transitivity
        l = len(update)
        for i in range(l-1, -1, -1):
            for j in range(i):
                if not is_sorted_pair(order, update[j], update[j+1]):
                    update[j], update[j+1] = update[j+1], update[j]
        res += update[l//2]
    return res



def main():
    data = get_input("input.txt")
    part1(*data)
    part2(*data)


def test():
    data = get_input("input.txt")
    assert part1(*data) == 6505
    assert part2(*data) == 6897

    data_test = get_input("test.txt")
    assert part1(*data_test) == 143
    assert part2(*data_test) == 123

    print("Test OK")


if __name__ == "__main__":
    test()
