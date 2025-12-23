import aoc.parse
from aoc import geometry as aoc_geometry
from aoc import aoc
from collections import defaultdict


def get_input(file):
    def get_info(line):
        ints = aoc.parse.get_ints(line)
        return (ints[0], ints[1]), (ints[2], ints[3])

    return aoc.parse.map_by_line(aoc.read_input(2022, 15, file), get_info)


@aoc.pretty_solution(1)
def part1(data, y):
    beacons_in_y = set()
    intervals = []
    for sensor, beacon in data:
        x_sensor, y_sensor = sensor
        x_beacon, y_beacon = beacon
        # compute radius of empty interval around xs
        radius = aoc_geometry.manhattan_distance(sensor, beacon) - abs(y - y_sensor)
        # if empty space doesn't intersect y continue
        if radius <= 0:
            continue
        # add interval of empty interval
        intervals.append((x_sensor - radius, x_sensor + radius))
        # NB since we're asked only to compute the empty space, we should keep count and then
        # remove the beacons in y
        if y_beacon == y:
            beacons_in_y.add(x_beacon)
    intervals = aoc_geometry.merge_intervals(intervals)
    return sum(hi - lo + 1 for lo, hi in intervals) - len(beacons_in_y)


@aoc.pretty_solution(2)
def part2(data, limit):
    # remap data as sensor, radius
    data = [(sensor, aoc_geometry.manhattan_distance(sensor, beacon)) for sensor, beacon in data]

    # not my idea.
    # NB the trick is that since we know there is exactly one possible point,
    # this must be exactly inside a 1-square regione insiede 4 lines, parallell and perpendicular 2
    # by 2. Hence if for each sensor we draw the 4 lines at distance r+1, then compute intersections
    # of the perpendicular, we are sure that the target is one on these intersections.
    # The we just check which is out of rech of every sensor
    # For each sensor, the 4 lines are (xs and y_sensor are sensor's coordinate and r the radius)
    #
    # y = y_sensor + (x - xs) + (r + 1) positive diagonal
    # y = y_sensor + (x - xs) - (r + 1) positive diagonal
    # y = y_sensor - (x - xs) + (r + 1) negative diagonal
    # y = y_sensor - (x - xs) - (r + 1) negative diagonal
    #
    # and we only need to store the intercepts (intersections with y-axis)
    positive_diagonals_intercept = defaultdict(int)
    negative_diagonals_intercept = defaultdict(int)
    for (x_sensor, y_sensor), r in data:
        r += 1
        positive_diagonals_intercept[y_sensor - x_sensor + r] += 1
        positive_diagonals_intercept[y_sensor - x_sensor - r] += 1
        negative_diagonals_intercept[y_sensor + x_sensor + r] += 1
        negative_diagonals_intercept[y_sensor + x_sensor - r] += 1

    # since the target must be inside the region formed by the 2 pairs, we can eliminate intercept
    # of single lines. Use only intercepts with at least 2 lines
    for a in (x for x, n in positive_diagonals_intercept.items() if n >= 2):
        for b in (x for x, n in negative_diagonals_intercept.items() if n >= 2):
            # intersection of y = x + a and y = -x + b is (b - a) / 2, (b + a) / 2
            intersection = (b - a) // 2, (b + a) // 2
            # check inside limit
            if all(0 <= coordinate <= limit for coordinate in intersection):
                # check candidate is actually the solution
                if all(aoc_geometry.manhattan_distance(intersection, sensor) > r for sensor, r in data):
                    return intersection[0] * 4000000 + intersection[1]
    return None


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    example = get_input("example.txt")
    assert part1(example, 10) == 26
    assert part2(example, 20) == 56000011

    data = get_input("input.txt")
    assert part1(data, 2000000) == 4748135
    assert part2(data, 4000000) == 13743542639657

    print("Test OK")


if __name__ == "__main__":
    test()
