from collections import deque
from advent_of_code.utils import geometry as aoc_geometry


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
