from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
import heapq

def get_input(file):
    raw = aoc.read_input(2023, 17, file)
    return aoc_parse.as_lines(raw)


def solve(grid, min_consecutives=0, max_consecutives=float('inf')):
    start, end = (0, 0), (len(grid) - 1, len(grid[0]) - 1)
    # init priority queue of nodes for Dijkstra
    # NB we bust keep track also of direction and consecutives moves in the same direction
    q = []
    # (dist, r, c, dr, dc, consecutive)
    # we could start east or south
    heapq.heappush(q, (0, *start, 0, 1, 0))
    heapq.heappush(q, (0, *start, 1, 0, 0))
    seen = set()
    while q:
        dist, r, c, dr, dc, consecutives = heapq.heappop(q)
        # check if over
        if (r, c) == end and consecutives >= min_consecutives:
            return dist
        # compute all possible new directions and new consecutive moves
        new_directions = []
        if consecutives < max_consecutives:
            # can follow same direction
            new_directions.append((dr, dc, consecutives + 1))
        # NB we're already making a step in the new direction
        # so 'consecutives' starts from 1
        # NB can steer only of already done 'min_consecutives' moves in same direction
        if dc == 0 and consecutives >= min_consecutives:
            new_directions.extend([(0, 1, 1), (0, -1, 1)])
        if dr == 0 and consecutives >= min_consecutives:
            new_directions.extend([(1, 0, 1), (-1, 0, 1)])
        # follow all possible directions and update q
        for new_dr, new_dc, new_consecutives in new_directions:
            new_r, new_c = r + new_dr, c + new_dc
            if not (0 <= new_r < len(grid) and 0 <= new_c < len(grid[0])):
                continue
            new_node = (new_r, new_c, new_dr, new_dc, new_consecutives)
            if new_node in seen:
                continue
            new_dist = dist + int(grid[new_r][new_c])
            heapq.heappush(q, (new_dist, *new_node))
            seen.add(new_node)


@aoc.pretty_solution(1)
def part1(grid):
    return solve(grid, max_consecutives=3)

@aoc.pretty_solution(2)
def part2(grid):
    return solve(grid, min_consecutives=4, max_consecutives=10)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 698
    assert part2(data) == 825
    print("Test OK")


if __name__ == "__main__":
    test()
