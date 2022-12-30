from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc


def get_input(file):
    lines = aoc_parse.as_lines(aoc.read_input(2022, 22, file))
    grid = {}
    start = None
    for r, line in enumerate(lines[:-2]):
        for c, point in enumerate(line):
            if point != " ":
                if not start:
                    start = c + 1j * r
                grid[c + 1j * r] = point == "."
    instructions = lines[-1].replace("R", " R ")
    instructions = instructions.replace("L", " L ")
    instructions = list(map(lambda c: int(c) if c.isnumeric() else c, instructions.split()))
    return start, grid, instructions


@aoc.pretty_solution(1)
def part1(data):
    pos, grid, path = data
    real_limits = {
        r: (
            min(point.real for point in grid if point.imag == r),
            max(point.real for point in grid if point.imag == r),
        )
        for r in set(p.imag for p in grid)
    }
    imag_limits = {
        c: (
            min(point.imag for point in grid if point.real == c),
            max(point.imag for point in grid if point.real == c),
        )
        for c in set(p.real for p in grid)
    }
    dir = 1
    for instruction in path:
        if isinstance(instruction, int):
            for _ in range(instruction):
                new_pos = pos + dir
                mod = None
                if (
                    dir.real == 0
                    and not imag_limits[new_pos.real][0]
                    <= new_pos.imag
                    <= imag_limits[new_pos.real][1]
                ):
                    mod = imag_limits[new_pos.real][1] - imag_limits[new_pos.real][0] + 1
                    new_imag = (new_pos.imag - imag_limits[new_pos.real][0]) % mod + imag_limits[
                        new_pos.real
                    ][0]
                    new_pos = new_pos.real + new_imag * 1j
                if (
                    dir.imag == 0
                    and not real_limits[new_pos.imag][0]
                    <= new_pos.real
                    <= real_limits[new_pos.imag][1]
                ):
                    mod = real_limits[new_pos.imag][1] - real_limits[new_pos.imag][0] + 1
                    new_real = (new_pos.real - real_limits[new_pos.imag][0]) % mod + real_limits[
                        new_pos.imag
                    ][0]
                    new_pos = new_real + new_pos.imag * 1j
                if not grid[new_pos]:
                    break
                pos = new_pos
        else:
            dir = dir * 1j if instruction == "R" else dir / 1j
    return 1000 * (1 + pos.imag) + 4 * (1 + pos.real) + {1: 0, 1j: 1, -1: 2, -1j: 3}[dir]


def compute_face(point, side):
    if point.imag < side:
        return 1
    if 2 * side <= point.imag:
        return 5 if point.real < 3 * side else 6
    if point.real < side:
        return 2
    if point.real < 2 * side:
        return 3
    return 4


def complex_modulo(x, mod):
    return (x.real % mod.real) + 1j * (x.imag % mod.imag)


@aoc.pretty_solution(2)
def part2(data):
    pos, grid, path = data
    side = min(point.real for point in grid if point.imag == 0) // 2
    faces = {}
    for face in range(1, 7):
        faces.update({face: set(point for point in grid if compute_face(point, side) == face)})
    dir = 1
    # face, relative position in face
    face_position = {
        1: 2 * side,
        2: side * 1j,
        3: side + side * 1j,
        4: 2 * side + side * 1j,
        5: 2 * side + 2 * side * 1j,
        6: 3 * side + 2 * side * 1j,
    }
    for instruction in path:
        if isinstance(instruction, int):
            for _ in range(instruction):
                new_pos = pos + dir
                new_dir = dir

                if new_pos not in grid:
                    pos_in_face = complex_modulo(pos, side + side * 1j)
                    face = compute_face(pos, side)
                    if dir == 1:
                        if face == 1:
                            new_face = 6
                            new_dir = -1
                            new_pos_in_face = side - 1 + 1j * (side - 1 - pos_in_face.imag)
                        if face == 4:
                            new_face = 6
                            new_dir = 1j
                            new_pos_in_face = (side - 1 - pos_in_face.imag) + 1j * 0
                        if face == 6:
                            new_face = 1
                            new_dir = -1
                            new_pos_in_face = (side - 1) + 1j * (side - 1 - pos_in_face.imag)
                    elif dir == -1:
                        if face == 2:
                            new_face = 6
                            new_dir = -1j
                            new_pos_in_face = (side - 1 - pos_in_face.imag) + 1j * (side - 1)
                        if face == 1:
                            new_face = 3
                            new_dir = 1j
                            new_pos_in_face = (pos_in_face.imag) + 1j * (0)
                        if face == 5:
                            new_face = 3
                            new_dir = -1j
                            new_pos_in_face = (side - 1 - pos_in_face.imag) + 1j * (side - 1)
                    elif dir == 1j:
                        if face == 2:
                            new_face = 5
                            new_dir = -1j
                            new_pos_in_face = (side - 1 - pos_in_face.real) + 1j * (side - 1)
                        if face == 3:
                            new_face = 5
                            new_dir = 1
                            new_pos_in_face = (0) + 1j * (side - 1 - pos_in_face.real)
                        if face == 5:
                            new_face = 2
                            new_dir = -1j
                            new_pos_in_face = (side - 1 - pos_in_face.real) + 1j * (side - 1)
                        if face == 6:
                            new_face = 2
                            new_dir = 1
                            new_pos_in_face = (0) + 1j * (side - 1 - pos_in_face.real)
                    elif dir == -1j:
                        if face == 2:
                            new_face = 1
                            new_dir = 1j
                            new_pos_in_face = (side - 1 - pos_in_face.real) + 1j * (0)
                        if face == 3:
                            new_face = 1
                            new_dir = 1
                            new_pos_in_face = (0) + 1j * (pos_in_face.real)
                        if face == 1:
                            new_face = 2
                            new_dir = 1j
                            new_pos_in_face = (side - 1 - pos_in_face.real) + 1j * (0)
                        if face == 6:
                            new_face = 4
                            new_dir = -1
                            new_pos_in_face = (side - 1) + 1j * (side - 1 - pos_in_face.real)

                    new_pos = face_position[new_face] + new_pos_in_face

                if not grid[new_pos]:
                    break
                pos = new_pos
                dir = new_dir
        else:
            dir = dir * 1j if instruction == "R" else dir / 1j
    return 1000 * (1 + pos.imag) + 4 * (1 + pos.real) + {1: 0, 1j: 1, -1: 2, -1j: 3}[dir]


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example) == 6032
    assert part2(example) == 5031

    data = get_input("input.txt")
    assert part1(data) == 97356
    assert part2(data) == None

    print("Test OK")


if __name__ == "__main__":
    test()
