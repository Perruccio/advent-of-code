from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2024, 5, file)
    order_raw, updates = raw.split("\n\n")
    order = set()
    for line in order_raw.split("\n"):
        a, b = map(int, line.split("|"))
        order.add((a, b))
    updates = [list(map(int, update.split(","))) for update in updates.split("\n")]
    return order, updates


def is_pair_sorted(order, a, b):
    # not transitive!! just check directly
    return (a, b) in order


def cmp(order, a, b):
    if is_pair_sorted(order, a, b):
        return -1
    if is_pair_sorted(order, b, a):
        return 1
    else:
        return 0
    

def is_vector_sorted(order, v):
    return all(is_pair_sorted(order, a, b) for a, b in zip(v, v[1:]))


@aoc.pretty_solution(1)
def part1(order, updates):
    return sum(v[len(v)//2] for v in updates if is_vector_sorted(order, v))


@aoc.pretty_solution(2)
def part2(order, updates):
    res = 0
    for update in updates:
        if is_vector_sorted(order, update):
            continue
        update.sort(key=cmp_to_key(lambda x, y:cmp(order, x, y)))
        l = len(update)
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
