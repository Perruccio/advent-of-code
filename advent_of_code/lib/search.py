from collections import deque, defaultdict
from advent_of_code.lib import geometry as aoc_geometry
from itertools import product

class Graph:
    def items(self):
        ...
    def __iter__(self):
        ...


def bfs_grid(grid, start, is_end, is_valid, exclude_diag=True):
    """Standard and not very efficient implementation of BFS in a grid.
    Returns the optimal path assuming every movement has equal cost and the grid
    is rectangular."""
    height, width = len(grid), len(grid[0])
    # store all visited nodes in a set to avoid recomputing
    visited = {start}
    # elements in the queue are (node, previous_node) to be able to reconstruct
    # optimal path
    q = deque([(start, None)])
    end = None
    # {node:previous node}
    prev_chain = {}
    while q:
        node, prev = q.popleft()
        prev_chain[node] = prev
        if is_end(grid, node):
            end = node
            break
        for neighbour in aoc_geometry.get_neighbours(node, (height, width), exclude_diag):
            if neighbour not in visited and is_valid(grid, neighbour, node):
                q.append((neighbour, node))
                visited.add(neighbour)

    # reconstruct optimal path backwards
    path = []
    while end in prev_chain:
        path.append(end)
        end = prev_chain[end]
    return path[::-1]


def floyd_warshall(graph : Graph):
    """Return a dict of dicts min_dists where min_dists[a][b] is the
    min weights to go from a to b in a directed graph.
    NB for now supports only edges with unitary weights"""
    # by default initialize nodes to have infinite distance
    min_dists = defaultdict(lambda: defaultdict(lambda: float("inf")))
    # first compute trivial cases
    for node, neighbours in graph.items():
        min_dists[node][node] = 0
        for neighbour in neighbours:
            # support only uniform weights
            min_dists[node][neighbour] = 1
            min_dists[neighbour][neighbour] = 0

    # the trick here is that min_dists is the min distance of nodes reachable
    # with only one step. After each loop of "mid", we're basically expanding to
    # include 2-steps paths, 3-steps paths, and so on, up to n-steps, because we're
    # using updated values of min_dists.
    # NB the order mid, src, dst of for loop is crucial!! we need
    # for mid in graph: (for src in graph: for dst in graph), where src and dest and
    # symmetric and interchangeable, but the first for loop must be relative to mid
    for mid, src, dst in product(graph, graph, graph):
        min_dists[src][dst] = min(min_dists[src][dst], min_dists[src][mid] + min_dists[mid][dst])

    return min_dists
