from advent_of_code.lib.all import *


def get_input(file):
    raw = aoc.read_input(2024, 9, file)
    return list(map(int, raw))


def checksum(mem):
    i = res = 0
    for id, n in mem:
        if id > 0:
            # id*i + id*(i+1) + id(i+2) = id * (i + (i+1) + (i+2)) = id * (n*i + (0+1+2))
            res += id * (i*n + n*(n-1)//2)
        i += n
    return res


@aoc.pretty_solution(1)
def part1(data_const):
    data = copy(data_const)
    assert(len(data)%2 == 1)
    mem = []
    # index of empty memory
    empty_i = 1
    # 2 pointer
    l, r = 0, len(data)-1
    while l <= r:
        # put from left pointer
        # id is just l//2 or r//2
        mem.append((l//2, data[l]))
        l += 2
        # fill empty space from right pointer
        # first handle case where empty space > right file size
        while data[r] < data[empty_i]:
            data[empty_i] -= data[r]
            mem.append((r//2, data[r]))
            r -= 2
            if r < l: break
        if r < l: break
        # break file (empty space is less than file size)
        mem.append((r//2, data[empty_i]))
        data[r] -= data[empty_i]
        empty_i += 2
    return checksum(mem)


@aoc.pretty_solution(2)
def part2(data):
    # create memory
    mem = []
    for i in range(0, len(data), 2):
        mem.append((i//2, data[i]))
        if i+1 < len(data):
            mem.append((-1, data[i+1]))
    # move files. NB mem len is modified during the loop,
    # we need a while to adjust the index accordingly
    r = len(mem)-1
    while r > 0:
        id, sz = mem[r]
        if id == -1:
            r -=1
            continue
        # search leftmost big enough empty space
        for l in range(r):
            id_l, sz_l = mem[l]
            # if not empty or not big enough, skip it
            if id_l != -1 or sz_l < sz:
                continue
            # split empty memory in 2 (where the leftmost is exactly the size of the file)
            if sz_l > sz:
                mem.insert(l, (id_l, sz))
                mem[l+1] = (id_l, sz_l - sz)
                # mem is longer now, we need to adjust r
                r += 1
            # swap
            mem[l], mem[r] = mem[r], mem[l]
            break
        r -= 1
    return checksum(mem)


def main():
    data = get_input("input.txt")
    part1(data)
    part2(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 6337367222422
    assert part2(data) == 6361380647183
    print("Test OK")


if __name__ == "__main__":
    test()
