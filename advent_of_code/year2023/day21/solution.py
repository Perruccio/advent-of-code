from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    raw = aoc.read_input(2023, 21, file)
    return aoc_parse.as_lines(raw)


@aoc.pretty_solution(1)
def part1(grid, max_steps = 64):
    # convert to complex
    # real part = colum, imag part = row (NB imag is pointing down)
    # we can also filter out the rocks and treat them as holes
    # in the grid
    grid = {c + r*1j : p for r, row in enumerate(grid) for c, p in enumerate(row) if p != "#"}
    start = next(filter(lambda p:grid[p] == "S", grid))
    # position, steps left
    q = [(start, max_steps)]
    seen = set()
    res = 0
    while q:
        pos, steps = node = q.pop()
        # skip if outside grid or already visited
        if pos not in grid or node in seen:
            continue
        # mark as visited
        seen.add(node)
        if steps == 0:
            # NB we can just increment res by 1
            # and not keep track of the set of end points
            # thanks to 'seen'. Any end point already visited
            # will be skipped
            res += 1
            continue
        # move to neighbours
        for delta in (1, -1, 1j, -1j):
            q.append((pos + delta, steps - 1))
    return res


@aoc.pretty_solution(2)
def part2(grid_l, max_steps=26501365):
    # assume a lot about the input..
    # start is at the center of a square with odd side length and
    # borders are empty. also vertical path and horizontal path from start are all empty
    grid = {c + r*1j : p for r, row in enumerate(grid_l) for c, p in enumerate(row) if p != "#"}
    start = next(filter(lambda p:grid[p] == "S", grid))
    # compute distance from start to the center of adjacent copies of the grid
    # distance from center to center
    c_to_c = int(2 * start.imag + 1)
    # distance from center of square to any angle
    c_to_a = c_to_c - 1
    # now i can travel directly from center to center
    # and if the steps left are > c_to_a, i can visit the whole new grid
    # NB we must pay attention to the fact that from start we must do an odd number of steps
    # hence only cells with odd manhattan distance are reachable. however, c_to_c is odd
    # which means that we can reach the complementary point of adjacent grid\, because max_steps - c_to_c
    # is even
    #
    # compute how many complete grids i can visit
    full_steps = max_steps - c_to_a
    furthest_grid = full_steps // c_to_c
    # compute in how many points i can stop if i have an even or odd number of steps left
    tot_even = part1(grid_l, c_to_a + (1 if c_to_a % 2 else 0))
    tot_odd = part1(grid_l, c_to_a + (0 if c_to_a % 2 else 1))
    res = [tot_even, tot_odd][max_steps % 2] # initial grid
    for g in range(0, furthest_grid + 1):
        res += 4 * g * [tot_even, tot_odd][(max_steps - g * c_to_c) % 2]
    print(res)


def main():
    data = get_input("input.txt")
    part1(data)
    # part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 3646
    # assert part2(data) == None
    print("Test OK")


if __name__ == "__main__":
    test()
