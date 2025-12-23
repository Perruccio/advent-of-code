from aoc.all import *

class Robot():
    def __init__(self, p, v):
        self.p = p
        self.v = v
    
    def move(self, n, rows, cols):
        self.p += n*self.v
        self.p = aoc.math.complex_modulo(self.p, cols + 1j*rows)

    def row(self):
        return int(self.p.imag)
    
    def col(self):
        return int(self.p.real)


def get_input(file):
    raw = aoc.read_input(2024, 14, file)
    robots = []
    for line in aoc.parse.as_lines(raw):
        px, py, vx, vy = aoc.parse.get_ints(line)
        robots.append(Robot(px + 1j*py, vx + 1j*vy))
    return robots


def simulate(robots, seconds, rows, cols):
    for robot in robots:
        robot.move(seconds, rows, cols)
    return robots


def show(robots, rows, cols):
    grid = [[" "]*cols for r in range(rows)]
    for robot in robots:
        grid[robot.row()][robot.col()] = "■"
    for line in grid:
        print(''.join(line))


@aoc.pretty_solution(1)
def part1(robots, seconds = 100):
    rows, cols = 103, 101
    robots = simulate(robots, seconds, rows, cols)
    quadrants = defaultdict(int)
    for robot in robots:
        x, y = robot.col(), robot.row()
        # discard robots in middle lines
        if x == cols//2 or y == rows//2:
            continue
        quad = x < cols//2, y < rows//2
        quadrants[quad] += 1
    return prod(quadrants.values())


@aoc.pretty_solution(2)
def part2(robots):
    rows, cols = 103, 101
    # skip first n cycles to speed up
    seconds = 7000
    robots = simulate(robots, seconds, rows, cols)
    for i in range(seconds+1, 10000):
        robots = simulate(robots, 1, rows, cols)
        if len(robots) == len(set(robot.p for robot in robots)):
            # show(robots, rows, cols)
            return i


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 224438715
    assert part2(data) == 7603
    print("Test OK")


if __name__ == "__main__":
    test()
