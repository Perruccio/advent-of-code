import pathlib

from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse


class IntegerPoint3D:
    __slots__ = "x", "y", "z"

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield from [self.x, self.y, self.z]

    @classmethod
    def create_integer_point_3d(cls, raw):
        return cls(*map(int, raw.split(",")))

    @staticmethod
    def adjacent(point1, point2):
        # exactly 2 equal coordinates
        equal_coordinates = sum(coord1 == coord2 for coord1, coord2 in zip(point1, point2))
        # exaclty 1 coordinate has distance exactly 1
        coords_dist_1 = sum(abs(coord1 - coord2) == 1 for coord1, coord2 in zip(point1, point2))
        return equal_coordinates == 2 and coords_dist_1 == 1


def get_input(file):
    return set(
        aoc_parse.map_input_lines(
            str(pathlib.Path(__file__).parent) + "/" + file, IntegerPoint3D.create_integer_point_3d
        )
    )


@aoc_output.pretty_solution(1)
def part1(data):
    tot_surface = 0
    points = set()
    for new_point in data:
        adjacents = sum(IntegerPoint3D.adjacent(point, new_point) for point in points)
        points.add(new_point)
        # add surface of new point (6 - adjacent) but also subtract adjacent from already counted surface
        # because it's now covered
        tot_surface += 6 - 2*adjacents
    return tot_surface


@aoc_output.pretty_solution(2)
def part2(data):
    pass


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 64
    assert part2(example) == 58

    data = get_input("input.txt")
    assert part1(data) == None
    # assert part2(data) == None

    print("Test OK")


if __name__ == "__main__":
    test()
