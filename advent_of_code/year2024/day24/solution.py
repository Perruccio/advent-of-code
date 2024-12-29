from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 24, file)
    raw_states, raw_conn = map(lambda s: s.splitlines(), raw.split("\n\n"))

    states = {}
    for wire, state in map(lambda line: line.split(": "), raw_states):
        states[wire] = int(state)
    
    conns = {}
    for line in raw_conn:
        x1, op, x2, _, res = line.split()
        conns[res] = (x1, op, x2)

    return states, conns


def operation(x, op, y):
    match op:
        case "AND": return x and y
        case "OR": return x or y
        case "XOR": return x != y


@aoc.pretty_solution(1)
def part1(states, conns):
    def get(z):
        if z in states:
            return states[z]
        x, op, y = conns[z]
        res = operation(get(x), op, get(y))
        states[z] = res
        return res
 
    res = 0
    for z in conns:
        if z.startswith("z") and get(z):
            res += 2**int(z[1:])
    return res


@aoc.pretty_solution(2)
def part2(states, conns):
    @cache
    def ancestors(wire):
        if wire in states:
            return set()
        a, _, b = conns[wire]
        res = set()
        res |= {a} if a in states else ancestors(a)
        res |= {b} if b in states else ancestors(b)
        return res

    res = []
    def check_z(z):
        # check z_n: one of the operand must be exactly x_n ^ y_n
        # the other is the carry, which must depend on (x_i, y_i) for i in [0, n-1]
        # operation must be XOR
        a, op, b = conns[z]
        if z == "z45":
            return True
        if op != "XOR":
            res.append(z)
            return False
        if z == "z00":
            return {a, b} == {"x00", "y00"}
        anc_a, anc_b = frozenset(ancestors(a)), frozenset(ancestors(b))
        n = int(z[1:])
        x_n, y_n = "x" + str(n).zfill(2), "y" + str(n).zfill(2)
        exp_anc_1 = frozenset({x_n, y_n})
        exp_anc_2 = frozenset({"x" + str(i).zfill(2) for i in range(0, n)} | {"y" + str(i).zfill(2) for i in range(0, n)})
        if anc_a == exp_anc_1 and anc_b == exp_anc_2:
            if conns[a][1] != "XOR":
                for conn in conns:
                    j, k, l = conns[conn]
                    if {j, l} == {x_n, y_n} and k == "XOR":
                        res.append(conn)
                res.append(a)
                return False
        if anc_b == exp_anc_1 and anc_a == exp_anc_2:
            if conns[b][1] != "XOR":
                for conn in conns:
                    j, k, l = conns[conn]
                    if {j, l} == {x_n, y_n} and k == "XOR":
                        res.append(conn)
                res.append(b)
                return False
        return False
    
    def is_z(wire):
        if wire == "z45":
            return True
        a, op, b = conns[wire]

        if op != "XOR":
            return False
        if {a, b} == {"x00", "y00"}:
            return True
        anc_a, anc_b = frozenset(ancestors(a)), frozenset(ancestors(b))
        for n in range(1, 46):
            exp_anc_1 = frozenset({"x" + str(n).zfill(2), "y" + str(n).zfill(2)})
            exp_anc_2 = frozenset({"x" + str(i).zfill(2) for i in range(0, n)} | {"y" + str(i).zfill(2) for i in range(0, n)})
            if {anc_a, anc_b} == {exp_anc_1, exp_anc_2}:
                return True
        return False

    for z_num in range(0, 46):
        check_z("z" + str(z_num).zfill(2))
    for conn in conns:
        if is_z(conn) and conn[0] != "z":
            res.append(conn)
    return ','.join(sorted(res))


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == 61495910098126
    assert part2(*data) == "css,cwt,gdd,jmv,pqt,z05,z09,z37"
    print("Test OK")


if __name__ == "__main__":
    test()
