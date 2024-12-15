from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 15, file)
    grid, moves = raw.split("\n\n")
    # real part = row, imag part 0 col
    m = {(i + 1j*j):p for i, line in enumerate(aoc_parse.as_lines(grid)) for j, p in enumerate(line)}
    moves = list(filter(lambda c: c != "\n", moves))
    return m, moves


def step(move):
    match move:
        case "<": return -1j
        case ">": return  1j
        case "^": return -1
        case "v": return  1
        case _: raise AssertionError("error")


@aoc.pretty_solution(1)
def part1(m, moves):
    # find start bot position
    bot = next(p for p, x in m.items() if x == "@")
    m[bot] = "."
    for d in map(step, moves):
        new = bot + d
        if m[new] == "#":
            continue
        if m[new] == ".":
            bot = new
            continue
        assert m[new] == "O"
        # find first empty spot
        while m[new] == "O":
            new += d
        # if found empty spot, shift all rocks by just swapping
        # the first with empty spot
        if m[new] == ".":
            m[new] = "O"
            m[bot+d] = "."
            bot += d
    # compute score
    res = 0
    for p, item in m.items():
        if item == "O":
            res += 100*p.real + p.imag
    return int(res)


def find_blocks(m, bot, step):
    # find blocks to move in case of vertical push
    # a block is represented by its left part "["
    q = [bot + step if m[bot + step] == "[" else bot + step -1j]
    # return set of all part of blocks to move (both left and right part)
    blocks = set()
    # DFS
    while q:
        block = q.pop()
        blocks.update({block, block + 1j})
        new = [block + step, block + 1j + step]
        if "#" in {m[p] for p in new}:
            # can't move
            return {}
        for x in new:
            if m[x] == "[":
                q.append(x)
            if m[x] == "]":
                q.append(x-1j)
    return blocks


def print_grid(m, bot):
    m = m|{bot:"@"}
    rows, cols = map(int, (1+max(p.real for p in m), 1+max(p.imag for p in m)))
    for r in range(rows):
        print(''.join([m[r+1j*c] for c in range(cols)]))
    print()


@aoc.pretty_solution(2)
def part2(m, moves):
    # widen items
    m2 = {}
    for p, item in m.items():
        r, c = map(int, (p.real, p.imag))
        # just map element in c to 2c and 2c+1
        c = 2*c
        m2[r + 1j*c] = item if item != "O" else "["
        if item == "@":
            m2[r + 1j*(c+1)] = "."
        else:
            m2[r + 1j*(c+1)] = item if item != "O" else "]"
    m = m2

    # find start bot position
    bot = next(p for p, x in m.items() if x == "@")
    m[bot] = "."
    for d in map(step, moves):
        new = bot + d
        if m[new] == "#":
            continue
        if m[new] == ".":
            bot += d
            continue
        assert m[new] in "[]"
        if d in (-1j, 1j):
            # horizontal push: similar to part1
            # find end of chain
            while m[new] in "[]":
                new += d
            if m[new] == "#":
                continue
            assert m[new] == "."
            # "pull" from end
            while new != bot:
                m[new] = m[new-d]
                new -= d
            bot += d
        else:
            # vertical push: find whole blocks to move
            blocks = find_blocks(m, bot, d)
            if not blocks:
                # can't move
                continue
            old_blocks = {block:m[block] for block in blocks}
            # remove from old map
            for block in blocks:
                m[block] = "."
            # add moved blocks
            m.update({block+d:old_blocks[block] for block in blocks})
            bot += d
    # compute score
    res = 0
    for p, item in m.items():
        if item == "[":
            res += 100*p.real + p.imag
    return res


def test():
    data = get_input("input.txt")
    assert part1(*deepcopy(data)) == 1486930
    assert part2(*data) == 1492011
    print("Test OK")


if __name__ == "__main__":
    test()
