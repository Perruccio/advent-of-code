from aoc.all import *


def get_input(file):
    raw = aoc.read_input(2025, 9, file)
    lines = aoc.parse.as_lines(raw)
    lines = [tuple(map(int, line.split(","))) for line in lines]
    return lines


def rect_area(p1, p2):
    return (1+ abs(p2[0] - p1[0])) * (1 + abs(p2[1] - p1[1]))


@aoc.pretty_solution(1)
def part1(data):
    # just brute force
    return max(rect_area(p1, p2) for p1, p2 in combinations(data, 2))


@aoc.pretty_solution(2)
def part2(red_tiles):
    # store all horizontal and vertical lines of the polygon
    h_lines = []
    v_lines = []
    for p1, p2 in zip(red_tiles, red_tiles[1:] + [red_tiles[0]]):
        r_start, r_end = min(p1[0], p2[0]), max(p1[0], p2[0])
        c_start, c_end = min(p1[1], p2[1]), max(p1[1], p2[1])
        if r_start == r_end:
            h_lines.append((r_start, c_start, c_end))
        elif c_start == c_end:
            v_lines.append((c_start, r_start, r_end))
        else:
            raise "not orthogonal line"

    # take all possible rectangles as couple of opposite red tiles
    rects = list(combinations(red_tiles, 2))
    # sort ascending by area (so we can be greedy later)
    rects.sort(reverse=True, key=lambda rect:rect_area(*rect))
    
    for p1, p2 in rects:
        # compute all 4 coordinates of the edges
        up, down = min(p1[0], p2[0]), max(p1[0], p2[0])
        left, right = min(p1[1], p2[1]), max(p1[1], p2[1])

        # check no intersection with all green lines
        valid = True

        # check horizontal lines
        for r, c_start, c_end in h_lines:
            if up < r < down and not (c_end <= left or c_start >= right):
                valid = False
                break

        if not valid:
            continue

        # check vertical lines
        for c, r_start, r_end in v_lines:
            if left < c < right and not (r_end <= up or r_start >= down):
                valid = False
                break
        
        if valid:
            return rect_area(p1, p2)

    return None


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 4750176210
    assert part2(data) == 1574684850
    print("Test OK")


if __name__ == "__main__":
    test()
