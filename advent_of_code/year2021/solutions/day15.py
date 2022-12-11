import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
import advent_of_code.utils.output as aoc_output
import advent_of_code.utils.parse as aoc_parse
import advent_of_code.utils.geometry as aoc_geometry
from collections import defaultdict
import heapq


def dijkstra(grid, scale=1):
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
    # the scale is used to extend the grid, repeating itself as a tile
    # in both directions

    # define cost function
    def cost(h, w, node, grid):
        ii, jj = node[0] // h, node[1] // w
        x = grid[node[0] % h][node[1] % w] + ii + jj
        return 1 + (x - 1) % 9

    # compute start and end points
    h, w = len(grid), len(grid[0])
    start, end = (0, 0), (h * scale - 1, w * scale - 1)

    # distance to minimize
    min_dist = defaultdict(lambda: float('inf'), {start: 0})

    # use prev to reconstruct path
    # prev = dict()

    visited = set()
    # priority queue
    pq = [(0, start)]
    while pq:
        # use heapq to get node with min distance in pq
        # this ensures that we can only visit every node once
        # therefore when we visit end we can exit
        dist, node = heapq.heappop(pq)

        # exit condition
        if node == end:
            return min_dist[end]

        # visit this node
        visited.add(node)

        # get neighbours of current node and update their distances
        for neigh in aoc_geometry.get_neighbours(node, (h * scale, w * scale), exclude_diag=True):
            # already solved
            if neigh in visited:
                continue

            # update distance if current path is better
            new_dist = dist + cost(h, w, neigh, grid)
            if new_dist < min_dist[neigh]:
                min_dist[neigh] = new_dist
                heapq.heappush(pq, (new_dist, neigh))
                # prev[neigh] = node
    return dist[end]  # , prev


def part1(data):
    return dijkstra(data)


def part2(data):
    return dijkstra(data, 5)


def main(pretty_print=True):
    def map_line(line):
        return list(map(int, line))

    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day15.txt', map_line)

    if pretty_print:
        aoc_output.print_result(1, part1, data)
        aoc_output.print_result(2, part2, data)
    else:
        return part1(data), part2(data)


if __name__ == "__main__":
    main()
