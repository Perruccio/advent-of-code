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
    sz = len(data)
    assert(sz%2 == 1)
    mem = []
    empty_i = 1
    l, r = 0, sz-1
    while l <= r and empty_i < len(data):
        # put from left pointer
        # id is just l//2 or r//2
        mem.append((l//2, data[l]))
        l += 2
        # fill empty space from right pointer
        # first handle case where empty space > right file
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
    # move file
    mem2 = mem[:]
    for j in range(len(mem)-1, 0, -2):
        id, sz = mem[j]
        for k, (id2, sz2) in enumerate(mem2):
            if id2 == id:
                break
            if id2==-1 and sz2 >= sz:
                mem2[k] = (-1, sz2-sz)
                g = mem2.index((id, sz))
                mem2[g] = (-1, sz)
                mem2.insert(k, (id, sz))
                break
    return checksum(mem2)


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
