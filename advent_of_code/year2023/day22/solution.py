from advent_of_code.lib.import_all import *


def get_input(file):
    raw = aoc.read_input(2023, 22, file)

    def parse_brick(line):
        coord = aoc_parse.get_ints(line)
        return [[coord[i], coord[i + 3]] for i in range(3)]

    return aoc_parse.map_by_line(raw, func=parse_brick)


def simulate(data):
    # sort by height
    data = sorted(data, key=lambda pp: min(pp[2]))
    bricks = list(map(lambda p: Cuboid(*p), data))
    # keep track of which bricks have highest point at a given z level
    levels = defaultdict(list)
    # two dictionary to keep track of depencies in terms of supporting the brick
    # key supports all bricks in value
    k_supports_v = defaultdict(set)
    # key is supported by all bricks in value
    v_supports_k = defaultdict(set)
    # simulate
    for i, brick in enumerate(bricks):
        # while above the ground
        while brick.zz[0] >= 1:
            # try to shift brick down
            brick.shift((0, 0, -1))
            # compute number of supports (intersections)
            inters = set(filter(lambda j: brick.intersect(bricks[j]) is not None, levels[brick.zz[0]]))
            if len(inters) > 0:
                for k in inters:
                    k_supports_v[k].add(i)
                    v_supports_k[i].add(k)
                break

        # shift up one step because loop ended when already too down
        brick.shift((0, 0, 1))
        levels[brick.zz[1]].append(i)

    return bricks, k_supports_v, v_supports_k


@aoc.pretty_solution(1)
def part1(data):
    bricks, k_supports_v, v_supports_k = simulate(data)

    # count all bricks i such that their upper supported
    # are supported also by other bricks
    res = 0
    for i in range(len(bricks)):
        res += all(len(v_supports_k[j]) >= 2 for j in k_supports_v[i])
    return res


@aoc.pretty_solution(2)
def part2(data):
    bricks, k_supports_v, v_supports_k = simulate(data)

    res = 0
    for b in range(len(bricks)):
        # compute the chain reaction after removing brick b
        # q is stack of falling bricks
        q = [b]
        fallen = set(q)
        while q:
            f = q.pop()
            res += 1
            # f is falling: take brick supported by f (not already fallen)
            # and check if no other bricks are supporting them
            # in this case, let them fall
            for upper in k_supports_v[f] - fallen:
                # other supporters of upper
                if v_supports_k[upper] <= fallen:
                    q.append(upper)
                    fallen.add(upper)
    # remove len(bricks) because we don't have to count
    # removed bricks but only consequent falls
    return res - len(bricks)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 522
    assert part2(data) == 83519
    print("Test OK")


if __name__ == "__main__":
    main()
