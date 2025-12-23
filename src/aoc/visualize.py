def print_image(image, empty="  ", full="* "):
    for line in image:
        for c in line:
            if c:
                print(full, end="")
            else:
                print(empty, end="")
        print()


def print_linked_list(node, end=" ", file=None):
    visited = set()
    while node and node not in visited:
        print(node.x, end=end, file=file)
        visited.add(node)
        node = node.right
    print()


def print_grid_from_complex(points: set[complex], empty=".", full="*", flip_y=False):
    """Print a grid from dict {complex:bool}. Can custom 'empty' and 'full' character, as well
    as flip_y to chooose if low y shuold be on top (don't flip) or bottom (flip)"""
    # normalize grid
    all_imags = set(p.imag for p in points)
    all_reals = set(p.real for p in points)
    min_y, max_y = int(min(all_imags)), int(max(all_imags))
    min_x, max_x = int(min(all_reals)), int(max(all_reals))
    height = max_y - min_y + 1
    width = max_x - min_x + 1
    # compute normalized grid
    grid = [[False for _ in range(width)] for _ in range(height)]
    for point in points:
        y = int(point.imag) - min_y
        y = height - 1 - y if flip_y else y
        grid[y][int(point.real) - min_x] = 1
    # print
    print_image(grid, empty=empty, full=full)
