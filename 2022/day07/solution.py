import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent
root = curr_dir.parent.parent
sys.path.append(str(root))

from utils import aoc
from collections import defaultdict


def get_input(file):
    return aoc.input_as_lines(str(curr_dir) + "/" + file)


class Directory:
    """Represent a directory, with size and a list of subfolders paths"""

    def __init__(self, size=0):
        self.size = size
        self.subs = []

    def add_sub(self, sub):
        self.subs.append(sub)


def parent_path(dir):
    return dir[:-1]


def sub_path(dir, subdir):
    """Return actual sub path if subdir != "..", else parent_path"""
    return parent_path(dir) if subdir == ".." else dir + (subdir, )


def do_ls(curr_dir, tree, input, i):
    """Extract information from command ls, compute size of current folder and its subfolders.
    The size of the subfolders will be computed lates."""

    # while reading output of ls (end of input or other command found)
    while i < len(input) and not input[i].startswith("$"):
        # input[i] is "<size> <file_name>"" or "'dir' <dir_name>"
        size_or_dir, item = input[i].split()
        if size_or_dir == "dir":
            tree[curr_dir].add_sub(sub_path(curr_dir, item))
        else:
            tree[curr_dir].size += int(size_or_dir)
        i += 1
    # return new index
    return i


def do(curr_dir, tree, input, i):
    """Execute command ('cd' or 'ls') and return the new state (directory, index)"""
    tokens = input[i].split()
    assert tokens[0] == "$"

    if tokens[1] == "cd":
        return sub_path(curr_dir, tokens[2]), i + 1
    elif tokens[1] == "ls":
        return curr_dir, do_ls(curr_dir, tree, input, i + 1)
    else:
        raise RuntimeError


def add_subfolder_size(tree, dir):
    """Recursevly add subfolders' size to each folder"""
    # dfs
    for sub_dir in tree[dir].subs:
        tree[dir].size += add_subfolder_size(tree, sub_dir)
    return tree[dir].size


def compute_tree(input):
    """Compute the tree of folders structure as a dictionary {path:Directory}"""

    # first step: compute folders tree with marginal size (contained files but not contained folders)
    # by executing one command at a time. Use tuples for paths
    tree = defaultdict(Directory)
    curr_dir, i = tuple(), 0
    while i < len(input):
        curr_dir, i = do(curr_dir, tree, input, i)

    add_subfolder_size(tree, ('/',))
    return tree


def part1(input, max_size=100000):
    tree = compute_tree(input)
    return sum([dir.size for dir in tree.values() if dir.size <= max_size])


def part2(input, tot_space=70000000, need=30000000):
    # compute single smallest directory that can be deleted to have at least
    # "need" free space
    tree = compute_tree(input)
    unused_space = tot_space - tree[('/',)].size
    need_to_free = need - unused_space
    return sorted([dir.size for dir in tree.values() if dir.size >= need_to_free])[0]


def main():
    input = get_input("input.txt")
    aoc.print_result(1, part1, input)
    aoc.print_result(2, part2, input)


def test():
    example = get_input("example.txt")
    assert part1(example) == 95437
    assert part2(example) == 24933642

    input = get_input("input.txt")
    assert part1(input) == 1644735
    assert part2(input) == 1300850
    print("Test OK")


if __name__ == "__main__":
    test()
