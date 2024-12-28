from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 21, file)
    return aoc_parse.as_lines(raw)


def step_to_key(step):
    match step:
        case  1 : return "v"
        case -1 : return "^"
        case  1j: return ">"
        case -1j: return "<"


def optimal_sequences(pad):
    # precompute optimal sequences for each pair of points
    # with BFS. result is such that res[(x, y)] = sequence of moves
    # that parent robot must signal to press y in this pad, given
    # that the finger is at x. it includes the final "A" for press
    res = defaultdict(list)
    for start, end in cart_prod(pad, repeat=2):
        if start == end:
            # we're already at the target button,
            # just press A
            res[(start, end)] = ["A"]
            continue
        # BFS
        q = deque([(start, "")])
        optimal = len(pad)
        while q:
            p, path = q.popleft()
            if p == end:
                res[(start, end)].append(path + "A")
                optimal = len(path)
                continue
            for step in (1, -1, 1j, -1j):
                new_p = p + step
                if new_p in pad and len(path) + 1 <= optimal:
                    q.append((new_p, path + step_to_key(step)))
    # convert to have result as buttons, not positions
    res = {(pad[x], pad[y]):paths for (x, y), paths in res.items()}
    return res


def convert_pad(pad):
    # convert pad to dictionary with complex keys
    res = {}
    for r, row in enumerate(pad):
        for c, button in enumerate(row):
            if button is not None:
                res[r + 1j*c] = button
    return res


def solve_num(code, seqs):
    # manually solve the first step from
    # numerical pad to first robot
    # return all possibile combinations (cartesian produt)
    res = [""]
    for pair in zip("A" + code, code):
        # cartesian product
        res = [last + seq for last in res for seq in seqs[pair]]
    return res


def solve(data, robots):
    num_pad = convert_pad([
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ])
    dir_pad = convert_pad([
        [None, "^", "A"],
        ["<", "v", ">"],
    ])
    num_seqs = optimal_sequences(num_pad)
    dir_seqs = optimal_sequences(dir_pad)

    @cache
    def min_length(seq, depth=robots):
        # return the min length of sequence that human must
        # input to result in 'seq' in the robot of depth 'depth':
        # the trick is that we can split the computation into optimal
        # for each single movement (from one button to another)
        if depth == 0:
            # human is reached
            return len(seq)
        res = 0
        # split the result in each pair that forms the sequence
        for pair in zip("A" + seq, seq):
            # for each pair, check what's the optimal number of human moves
            # by brute forcing all sequences of the parent robot recursively
            res += min(min_length(subseq, depth - 1) for subseq in dir_seqs[pair])
        return res

    # compute final score
    res = 0
    for code in data:
        # manually solve last step for numerical pad
        dir_last = solve_num(code, num_seqs)
        best = min(map(min_length, dir_last))
        res += best * int(code[:-1])
    return res


@aoc.pretty_solution(1)
def part1(data):
    return solve(data, 2)


@aoc.pretty_solution(2)
def part2(data):
    return solve(data, 25)


def test():
    data = get_input("input.txt")
    assert part1(deepcopy(data)) == 217662
    assert part2(data) == 263617786809000
    print("Test OK")


if __name__ == "__main__":
    test()
