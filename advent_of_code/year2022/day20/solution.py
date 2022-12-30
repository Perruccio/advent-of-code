from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import algorithm as aoc_algo
from advent_of_code.lib import aoc


class Node:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None


def get_input(file):
    return aoc_parse.map_by_line(aoc.read_input(2022, 20, file), int)


def solve(data, key=1, times=1):
    n = len(data)
    # use a vector of nodes to remember original order
    nodes = [Node(val * key) for val in data]
    for i in range(n):
        nodes[i].right = nodes[(i + 1) % n]
        nodes[i].left = nodes[i - 1]

    # NB we must use mod n-1 because when we want to remove a node,
    # we're left with n-1 nodes
    mod = n - 1
    for t in range(times):
        for node in nodes:
            # we need to remember node with value 0 for answer
            if node.x == 0 and t == times - 1:
                node_0 = node
                continue

            # advance (left or right) until new position is reached
            # instead of just performing node.x jumps, check which direction
            # is shorter (nice performance gain)
            # NB we're making jumps to the left, do one more jump, so that new is always
            # at the left of where we should insert node

            # first compute right jumps
            jumps = (node.x % mod + mod) % mod
            # check if going left would be better (remember to do one jump more)
            if mod - jumps + 1 < jumps:
                jumps -= mod + 1
            new = aoc_algo.advance_in_linked_list(node, jumps)

            if new == node:
                continue

            # remove node from previous position and connect adjacent
            node.right.left = node.left
            node.left.right = node.right

            # add old node in-between of new neighbours
            node.right = new.right
            node.left = new
            new.right.left = node
            new.right = node

    # compute answer
    res = 0
    for _ in range(3):
        for _ in range(1000):
            node_0 = node_0.right
        res += node_0.x
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, key=811589153, times=10)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 3
    assert part2(example) == 1623178306

    data = get_input("input.txt")
    assert part1(data) == 872
    assert part2(data) == 5382459262696

    print("Test OK")


if __name__ == "__main__":
    test()
