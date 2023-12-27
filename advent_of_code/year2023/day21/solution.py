from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from collections import deque


def get_input(file):
    raw = aoc.read_input(2023, 21, file)
    return aoc_parse.as_lines(raw)


def count_reachable(grid, start, max_steps):
    # convert to complex
    # real part = colum, imag part = row (NB imag is pointing down)
    # we can also filter out the rocks and treat them as holes
    # in the grid
    grid = {c + r*1j : p for r, row in enumerate(grid) for c, p in enumerate(row) if p != "#"}
    # position, steps left
    q = deque([(start[1] + start[0]*1j, max_steps)])
    # NB we could use DFS, but with BFS we can make sure not to ever
    # return to already visited points
    # set of points already visited
    seen = set()
    res = 0
    while q:
        pos, steps = q.popleft()
        # skip if outside grid or already visited
        if pos not in grid or pos in seen:
            continue
        # mark as visited
        seen.add(pos)
        # NB this position is reachable if steps is either 0 or even,
        # because i could go back and forth.
        # this trick allows us to avoid returning to already visited points
        if steps % 2 == 0:
            # NB we can just increment res by 1
            # and not keep track of the set of end points
            # thanks to 'seen'. Any end point already visited
            # will be skipped
            res += 1
        if steps == 0:
            continue
        # move to neighbours
        for delta in (1, -1, 1j, -1j):
            q.append((pos + delta, steps - 1))
    return res


@aoc.pretty_solution(1)
def part1(grid):
    start = next((r, c) for r, row in enumerate(grid) for c, p in enumerate(row) if p == "S")
    return count_reachable(grid, start, 64)


@aoc.pretty_solution(2)
def part2(grid, max_steps=26501365):
    # assume a lot about the input..
    # start is at the center of a square with odd side length and
    # borders are empty. also vertical path and horizontal path from start are all empty
    # compute distance from start to the center of adjacent copies of the grid
    # distance from center to center
    res = 0
    side = len(grid)
    # assert empty columns, rows, sparse
    assert side == len(grid[0])
    # NB !! if i go straight in any direction from center (start), i'd reach exactly the boundary
    # of a copy of grid
    assert max_steps % side == side // 2
    # NB starting grid and extreme grid are not totally covered
    whole_grids = max_steps // side - 1
    # NB side is odd -> from center to center i make odd steps ->
    # parity of reachable cells change like in a chess board
    assert side % 2 == 1
    # reachable points if odd steps are left
    assert max_steps % 2 == 1
    start = next((r, c) for r, row in enumerate(grid) for c, p in enumerate(row) if p == "S")

    # compute total odd and even grids
    reachable_odd = count_reachable(grid, start, 2*side + 1)
    reachable_even = count_reachable(grid, start, 2*side)
    # the following odd number squared 
    tot_odd = (whole_grids // 2 * 2 + 1)**2
    # the following even number squared 
    tot_even = ((whole_grids + 1) // 2 * 2)**2
    res += tot_even * reachable_even + tot_odd * reachable_odd

    # now compute and add the for the corners
    left_steps_corner = side - 1
    corner_north = count_reachable(grid, (side - 1, start[1]), left_steps_corner)
    corner_east = count_reachable(grid, (start[0], 0), left_steps_corner)
    corner_south = count_reachable(grid, (0, start[1]), left_steps_corner)
    corner_west = count_reachable(grid, (start[0], side - 1), left_steps_corner)
    res += corner_north + corner_east + corner_west + corner_south

    # compute small broken grids on diagonals
    n_small = whole_grids + 1
    left_steps_small = left_steps_corner - side // 2 - 1
    # north-est, south-est, ...
    small_ne = count_reachable(grid, (side - 1, 0), left_steps_small)
    small_nw = count_reachable(grid, (side - 1, side - 1), left_steps_small)
    small_se = count_reachable(grid, (0, 0), left_steps_small)
    small_sw = count_reachable(grid, (0, side - 1), left_steps_small)
    res += n_small * (small_ne + small_se + small_sw + small_nw)

    # compute large broken grids on diagonals
    n_large = whole_grids
    left_steps_large = left_steps_small + side
    # north-est, south-est, ...
    large_ne = count_reachable(grid, (side - 1, 0), left_steps_large)
    large_se = count_reachable(grid, (0, 0), left_steps_large)
    large_sw = count_reachable(grid, (0, side - 1), left_steps_large)
    large_nw = count_reachable(grid, (side - 1, side - 1), left_steps_large)
    res += n_large * (large_ne + large_se + large_sw + large_nw)
    
    return res


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 3646
    assert part2(data) == 606188414811259
    print("Test OK")


if __name__ == "__main__":
    test()
