from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 12, file).split("\n\n")
    shapes = raw[:5]
    shapes = list(map(lambda s:s.split(":\n")[1], shapes))
    shapes = [list(shape.split("\n")) for shape in shapes]

    regions = raw[-1].split("\n")
    regions = [aoc.parse.get_ints(area) for area in regions]
    return shapes, regions


@aoc.pretty_solution(1)
def part1(data):
    shapes, regions = data
    # it turns out that we don't need any kind of optimization
    # just put the shapes one after the other
    max_shape_area = max(len(shape)*len(shape[0]) for shape in shapes)

    res = 0
    for height, width, *n_shapes in regions:
        if max_shape_area * sum(n_shapes) <= height*width:
            res += 1
    return res
    

def main():
    data = get_input("input.txt")
    part1(deepcopy(data))


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 476
    print("Test OK")


if __name__ == "__main__":
    main()
