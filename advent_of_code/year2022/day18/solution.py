import pathlib
from attr import dataclass
from advent_of_code.utils import output as aoc_output
from advent_of_code.utils import parse as aoc_parse


@dataclass(frozen=True)
class IntegerPoint3D:
    """Represent a point with integer coordinates in the 3D space.
    NB can also be used to represent unitary cube"""
    x: int
    y: int
    z: int

    @classmethod
    def create_integer_point_3d(cls, raw):
        return cls(*map(int, raw.split(",")))

    def __iter__(self):
        yield from [self.x, self.y, self.z]

    def sides(self):
        """Return the 6 sides of a cube as cubes"""
        shifts = [-1, 0, 1]
        for dx in shifts:
            for dy in shifts:
                for dz in shifts:
                    # NB we want the 6 sides, so only one among dx, dy, dz must be nonzero
                    if (dx, dy, dz).count(0) == 2:
                        yield IntegerPoint3D(self.x + dx, self.y + dy, self.z + dz)


def get_input(file):
    return set(
        aoc_parse.map_input_lines(
            str(pathlib.Path(__file__).parent) + "/" + file, IntegerPoint3D.create_integer_point_3d
        )
    )


def tot_surface(cubes):
    # for each point add sides that are not in cubes
    return sum((side not in cubes) for cube in cubes for side in cube.sides())


@aoc_output.pretty_solution(1)
def part1(cubes):
    return tot_surface(cubes)


@aoc_output.pretty_solution(2)
def part2(data):
    # compute "all" data of cuboid enclosing data, then remove outer and surface (leaving us
    # with the inside space inside obsidian) then compute surface of inside space inside

    # NB add +-1 to be sure of having the space to correctly visit all outer data
    # during DFS
    min_x, min_y, min_z = min_limits = list(map(lambda v: min(v) - 1, zip(*data)))
    max_x, max_y, max_z = max_limits = list(map(lambda v: max(v) + 1, zip(*data)))

    # all data = outer (enclosing cuboid) + surface of obsidian + inside inside obsidian
    all_cubes = set(
        IntegerPoint3D(x, y, z)
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y + 1)
        for z in range(min_z, max_z + 1)
    )

    # DFS to compute outer data of obsidian
    air = set()
    todo = [IntegerPoint3D(min_x, min_y, min_z)]
    while todo:
        cube = todo.pop()
        # exclude cubes in data (obsidian surface) and already seen in air
        for side in set(cube.sides()) - data - air:
            # check that side cube is within air
            if not all(left <= p <= right for left, p, right in zip(min_limits, side, max_limits)):
                continue
            todo.append(side)
            air.add(side)

    # inside space inside obsidian
    inside = all_cubes - air - data
    return tot_surface(data) - tot_surface(inside)


def main():
    cubes = get_input("input.txt")
    part1(cubes)
    part2(cubes)


def test():
    assert part1(set((IntegerPoint3D(1, 1, 1), IntegerPoint3D(2, 1, 1)))) == 10

    example = get_input("example.txt")
    assert part1(example) == 64
    assert part2(example) == 58

    cubes = get_input("input.txt")
    assert part1(cubes) == 3494
    assert part2(cubes) == 2062

    print("Test OK")


if __name__ == "__main__":
    test()
