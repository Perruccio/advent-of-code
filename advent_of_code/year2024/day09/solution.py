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
    # following hyper neutrino's approach
    # create memory: store files in a dictionary with id as key
    # and empty space in a list
    files = {}
    empty = []
    pos = 0
    for i in range(0, len(data), 2):
        file_id = i//2
        # file
        assert(data[i] > 0)
        files[file_id] = (pos, data[i])
        pos += data[i]
        # empty
        if i+1 < len(data) and data[i+1] > 0:
            empty.append((pos, data[i+1]))
            pos += data[i+1]
    # move files
    for file_id in range(max(files.keys()), 0, -1):
        file_pos, file_sz = files[file_id]
        for i, (empty_pos, empty_sz) in enumerate(empty):
            if empty_pos > file_pos:
                break
            if empty_sz >= file_sz:
                files[file_id] = (empty_pos, file_sz)
                if empty_sz == file_sz:
                    del empty[i]
                else:
                    empty[i] = (empty_pos + file_sz, empty_sz - file_sz)
                break
    # compute checksum
    res = 0
    for id, (pos, sz) in files.items():
        for i in range(pos, pos + sz):
            res += id*i
    return res


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
