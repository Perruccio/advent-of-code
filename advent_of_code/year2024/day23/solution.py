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


def dfs(n, graph):
    # find largest connected component that includes node n
    q = [(n, frozenset({n}))]
    seen = {q[0][1]}
    while q:
        node, req = q.pop()
        for nb in graph[node]:
            # already included
            if nb in req: continue
            # not fully connected
            if not req <= graph[nb]: continue
            new = frozenset(req | {nb})
            if new in seen: continue
            seen.add(new)
            q.append((nb, new))
    return max(seen, key=len)

    
@aoc.pretty_solution(2)
def part2(graph):
    largest = set()
    for n in graph:
        group = dfs(n, graph)
        if len(group) > len(largest):
            largest = group
    return ','.join(sorted(largest))
    

def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 1151
    assert part2(data) == "ar,cd,hl,iw,jm,ku,qo,rz,vo,xe,xm,xv,ys"
    print("Test OK")


if __name__ == "__main__":
    test()
