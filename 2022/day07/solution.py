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
    """Represent a directory, with marginal size (contained files), a list of sub-Directories,
    and size = total size (files + subfolders)"""

    def __init__(self):
        self.marginal_size = 0
        self.subs = []
        self.size = None

    def add_sub(self, sub):
        self.subs.append(sub)

    def get_size(self):
        if self.size is None:
            self.size = self.marginal_size + sum(sub.get_size() for sub in self.subs)
        return self.size


def change_dir(dir, subdir):
    """Return actual sub path if subdir != "..", else parent_path"""
    return dir[:-1] if subdir == ".." else dir + (subdir,)


def compute_tree(input):
    """Compute the tree of folders structure as a dictionary {path:Directory}"""

    # first step: compute folders tree with marginal size (contained files but not contained folders)
    # by executing one command at a time. Use tuples for paths
    tree = defaultdict(Directory)
    current = tuple()  # current path as tuple
    for line in input:
        match line.split():
            case ["$", "cd", dir]:
                current = change_dir(current, dir)
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                # add the subfolder to the tree and link it to current
                tree[current].add_sub(tree[change_dir(current, name)])
            case [size, name]:
                tree[current].marginal_size += int(size)
            case _:
                raise RuntimeError
    return tree


def part1(input, max_size=100000):
    tree = compute_tree(input)
    return sum([dir.get_size() for dir in tree.values() if dir.get_size() <= max_size])


def part2(input, tot_space=70000000, need=30000000):
    # compute single smallest directory that can be deleted to have at least
    # "need" free space
    tree = compute_tree(input)
    need_to_free = need - (tot_space - tree[("/",)].get_size())
    return min(
        [dir.get_size() for dir in tree.values() if dir.get_size() >= need_to_free]
    )


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
