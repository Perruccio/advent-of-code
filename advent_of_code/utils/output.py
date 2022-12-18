import time


def print_result(part, func, *arg, **kw):
    t = time.time_ns()
    ans = func(*arg, **kw)
    ns = time.time_ns() - t  # nanoseconds
    print(f"Part {part}: {ans} \t({time_measure(ns)})")
    return ans


def pretty_solution(part):
    def decorator(func):
        def wrapper(*arg, **kw):
            t = time.time_ns()
            ans = func(*arg, **kw)
            ns = time.time_ns() - t  # nanoseconds
            if isinstance(ans, list):
                print(f"Part {part}: \t({time_measure(ns)})")
                for line in ans:
                    print(line)
            else:
                print(f"Part {part}: {ans} \t({time_measure(ns)})")
            return ans

        return wrapper

    return decorator


def time_measure(ns):
    # compute appropriate time measure units
    i = 0
    while ns >= 1000 and i < 3:
        ns /= 1000
        i += 1
    return str(f"{ns:.2f}") + " " + ["ns", "us", "ms", "s"][i]


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


def print_grid_from_complex(points: dict[complex], empty=".", full="*", flip_y=False):
    """Print a grid from dict {complex:bool}. Can custom 'empty' and 'full' character, as well
    as flip_y to chooose if low y shuold be on top (don't flip) or bottom (flip)"""
    # normalize grid
    min_y = int(min(key.imag for key, value in points.items() if value))
    max_y = int(max(key.imag for key, value in points.items() if value))
    min_x = int(min(key.real for key, value in points.items() if value))
    max_x = int(max(key.real for key, value in points.items() if value))
    height = max_y - min_y + 1
    width = max_x - min_x + 1
    # compute normalized grid
    grid = [[False for _ in range(width)] for _ in range(height)]
    for point, value in points.items():
        if value:
            y = int(point.imag) - min_y
            y = height - 1 - y if flip_y else y
            grid[y][int(point.real) - min_x] = value
    # print
    print_image(grid, empty=empty, full=full)
