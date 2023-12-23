from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from copy import deepcopy


def get_input(file):
    raw = aoc.read_input(2023, 19, file)
    workflow, parts_raw = raw.split("\n\n")
    process = {}
    parts = []
    for flow in workflow.split("\n"):
        name, rules = flow[:-1].split("{")
        process[name] = list(map(lambda r: r.split(":"), rules.split(",")))
        process[name][-1] = process[name][-1][0]
    for part in parts_raw.split("\n"):
        parts.append(tuple(map(lambda s: int(s[2:]), part[1:-1].split(","))))
    return process, parts


@aoc.pretty_solution(1)
def part1(data):
    flows, parts = data
    res = 0
    # just simulate the process
    for x, m, a, s in parts:
        curr = "in"
        while curr not in ["A", "R"]:
            for rule in flows[curr][:-1]:
                # follow new flow if condition is met
                if eval(rule[0]):
                    curr = rule[1]
                    break
            else:
                curr = flows[curr][-1]
        # if A compute score, ignore if R
        if curr == "A":
            res += x + m + a + s
    return res


def add_constraint(xmas_bounds, constraint):
    # add constraint to xmas_bound
    # take the intersection
    # NB modify in place
    var = constraint[0]  # "x", "m", "a" or "s"
    bound = constraint[1]  # ">" or "<"
    value = int(constraint[2:])
    idx = "xmas".find(var)  # find to which variable we shuold add
    if bound == "<":
        xmas_bounds[idx][1] = min(value - 1, xmas_bounds[idx][1])
    else:
        xmas_bounds[idx][0] = max(value + 1, xmas_bounds[idx][0])
    return xmas_bounds


def negative_constraint(constraint):
    # return the negation of a given constraint
    # eg s<5 -> s>4
    bound = constraint[1]
    value = int(constraint[2:])
    new_bound = "<" if bound == ">" else ">"
    new_value = value - 1 if bound == "<" else value + 1
    return constraint[0] + new_bound + str(new_value)


@aoc.pretty_solution(2)
def part2(data):
    # follow all the possible paths of the flows
    # starting from "in". for every flow, update
    # the possible values of xmas as (lower_bound, upper_bound)
    # always taking the intersection with previous values.
    # NB when following the rules of a flow, remeber to keep track
    # of the negations of the rules, that must be applied to the next rules
    flows, parts = data
    res = 0
    mn, mx = 1, 4000
    # current flow + all lower and upper bounds (inclusive)
    q = [("in", *[[mn, mx] for _ in range(4)])]
    while q:
        # curr, xmas = [xx, mm, aa, s]
        curr, *xmas = q.pop()
        # skip if rejected
        if curr == "R":
            continue
        # skip if impossible path (max < min)
        # it actually isnt necessary for input
        for lo, hi in xmas:
            impossible = False
            if lo > hi:
                impossible = True
                break
        if impossible:
            continue
        # compute score if accepted
        if curr == "A":
            score = 1
            for lo, hi in xmas:
                score *= hi - lo + 1
            res += score
            continue

        # follow all possible paths from current node
        # NB keep track of the negation of all encounterd rules
        # because they must be applied to next nodes
        for rule, nxt in flows[curr][:-1]:
            this_xmas = deepcopy(xmas)
            add_constraint(this_xmas, rule)
            # follow this path
            q.append((nxt, *this_xmas))
            # add the negatives to xmas and go on
            # NB we can continue to modify the same xmas of the current node
            add_constraint(xmas, negative_constraint(rule))

        # manually handle last possibility: no rule, just go to next flow
        q.append((flows[curr][-1], *xmas))
    return res


def main():
    data = get_input("example.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 395382
    assert part2(data) == 103557657654583
    print("Test OK")


if __name__ == "__main__":
    test()
