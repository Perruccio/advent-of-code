from advent_of_code.lib.import_all import *
import sympy as sp


def get_input(file):
    raw = aoc.read_input(2023, 24, file)
    return aoc_parse.map_by_line(raw, func=aoc_parse.get_ints)


@aoc.pretty_solution(1)
def part1(data, min_coord=200000000000000, max_coord=400000000000000):
    res = 0
    for i, (x1, y1, z1, vx1, vy1, vz1) in enumerate(data):
        assert vx1 != 0
        m1 = vy1 / vx1
        for x2, y2, z2, vx2, vy2, vz2 in data[i+1:]:
            assert vx2 != 0
            m2 = vy2 / vx2
            if m1 == m2:
                continue
            # solved with pen and paper
            x_inters = (y2 - y1 - x2*m2 + x1 * m1 ) / (m1 - m2)
            y_inters = y1 + m1 * x_inters - x1 * m1
            # skip if intersection not in boundaries
            if not all(min_coord <= coord <= max_coord for coord in (x_inters, y_inters)):
                continue
            # check intersection is in the future
            if sign(x_inters - x1) == sign(vx1) and sign(x_inters - x2) == sign(vx2):
                res += 1
    return res


@aoc.pretty_solution(2)
def part2(data):
    # https://www.youtube.com/watch?v=guOyA7Ijqgk&t=3s
    # the unknown rock position and rock velocity
    # (x, y, z, vx, vy, vz) must solve
    #
    # x + vx * t_i = x_i + vx_i * t_i
    # y + vy * t_i = y_i + vy_i * t_i
    # z + vz * t_i = z_i + vz_i * t_i
    #
    # for each i-th hail.
    # Isolate -t_i from the 3 equations and we get
    #
    # (x - x_i) / (vx - vx_i) = (y - y_i) / (vy - vy_i) = (z - z_i) / (vz - vz_i)
    #
    # for each i.

    x, y, z, vx, vy, vz = sp.symbols("x, y, z, vx, vy, vz")

    equations = []
    # 10 equations shohld be sufficient for 6 variables
    for x_i, y_i, z_i, vx_i, vy_i, vz_i in data[:10]:
        equations.append((x - x_i) / (vx - vx_i) - (y - y_i) / (vy - vy_i))
        equations.append((y - y_i) / (vy - vy_i) - (z - z_i) / (vz - vz_i))

    solutions = sp.solve(equations)[0]
    return sum(solutions[c] for c in (x, y, z))


def main():
    data = get_input("example.txt")
    part1(data, 7, 27)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 15558
    assert part2(data) == 765636044333842
    print("Test OK")


if __name__ == "__main__":
    test()
