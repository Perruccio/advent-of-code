from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 23, file)
    edges = aoc_parse.map_by_line(raw, lambda line:line.split("-"))
    graph = defaultdict(set)
    for n1, n2 in edges:
        graph[n1].add(n2)
        graph[n2].add(n1)
    return graph


@aoc.pretty_solution(1)
def part1(graph):
    triangles = set()
    # brute force all triangles
    for n1, ns in graph.items():
        # check if neighbours n2, n3 of n1 are connected
        # count only if valid (any of the nodes start with "t")
        for n2, n3 in combinations(ns, 2):
            if n3 in graph[n2] and any(n.startswith("t") for n in (n1, n2, n3)):
                triangles.add(frozenset({n1, n2, n3}))
    return len(triangles)


def lazy_intersect(set1, set2):
    yield from set(set1) & set(set2)


def clique(candidates, size, graph):
    # return the list of a clique of size 'size' composed
    # by nodes in 'candidates'

    # recursion base case
    if size == 0:
        return []
    # try each node in candidates
    for v in candidates:
        # if v is in the clique, then we must restrict to its friends
        res = clique(lazy_intersect(candidates, graph[v]), size-1, graph)
        if res != None:
            return res + [v]
    return None

    
@aoc.pretty_solution(2)
def part2(graph):
    largest = []
    max_clique_size = max(map(len, graph.values())) + 1
    for i in range(1, max_clique_size + 1):
        # find clique of size i
        clique_i = clique(set(graph), i, graph)
        if clique_i and len(clique_i) > len(largest):
            largest = clique_i
    return ','.join(sorted(largest))
    

def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 1151
    assert part2(data) == "ar,cd,hl,iw,jm,ku,qo,rz,vo,xe,xm,xv,ys"
    print("Test OK")


if __name__ == "__main__":
    test()
