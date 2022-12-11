def sorted_string(s):
    s = sorted(s)
    return "".join(s)


def sum_grid(grid):
    """Compute the sum of all values in a grid (list of list)"""
    return sum(sum(value for value in row) for row in grid)


def map_grid(func, grid):
    """Apply function to every element of a grid"""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            grid[r][c] = func(grid[r][c])
    return grid
