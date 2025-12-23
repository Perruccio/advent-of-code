from aoc.all import *
import math


def get_input(file):
    raw = aoc.read_input(2025, 8, file)
    lines = raw.splitlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def dist(p1, p2):
    return math.hypot(*[a - b for a, b in zip(p1, p2)])


## naive implementation of union-find
def root(i, parent):
    if parent[i] == i:
        return i
    # optimization: avoid linear trees
    # set the parent directly
    parent[i] = root(parent[i], parent)
    return parent[i]


def merge(i, j, parent):
    parent[root(i, parent)] = root(j, parent)


@aoc.pretty_solution(1)
def part1(data):
    connections = 1000
    # just use indices of points instead of actual 3d points
    edges = list(combinations(range(len(data)), 2))
    dists = sorted(edges, key=lambda ii: dist(data[ii[0]], data[ii[1]]))
    
    # init union-find
    parent = list(range(len(data)))

    # do the work
    for p1, p2 in dists[:connections]:
        merge(p1, p2, parent)

    # find size of each subsets
    sizes = [0] * len(data)
    for i in range(len(data)):
        sizes[root(i, parent)] += 1

    return prod(sorted(sizes)[-3:])


@aoc.pretty_solution(2)
def part2(data):
    # just use indices of points instead of actual 3d points
    edges = list(combinations(range(len(data)), 2))
    dists = sorted(edges, key=lambda ii: dist(data[ii[0]], data[ii[1]]))
    
    # init union-find
    parent = list(range(len(data)))

    # do the work
    circuits = len(data)
    for p1, p2 in dists:
        if root(p1, parent) == root(p2, parent):
            continue
        merge(p1, p2, parent)
        circuits -= 1
        if circuits == 1:
            break

    # find size of each subsets
    return data[p1][0] * data[p2][0]


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 115885
    assert part2(data) == 274150525
    print("Test OK")


if __name__ == "__main__":
    main()
