import pathlib

prj_path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
from advent_of_code.lib import parse as aoc_parse
from advent_of_code.lib import aoc
from math import floor, ceil


def furthest_node(tree, dir):
    """ return most right or left node of tree"""

    def advance(node, dir):
        return node.right if dir == 'right' else node.left

    while advance(tree, dir) is not None:
        tree = advance(tree, dir)
    return tree


class Tree:
    """ a binary tree, leaf nodes are trees with non-None leaf attribute
    store also the parent as attribute"""

    def __init__(self, node):
        if isinstance(node, int):
            self.leaf = node
            self.left, self.right = None, None
        else:
            self.left = node[0] if isinstance(node[0], Tree) else Tree(node[0])
            self.right = node[1] if isinstance(node[1], Tree) else Tree(node[1])
            self.left.parent, self.right.parent = self, self
            self.leaf = None
        self.parent = None

    def __str__(self):
        if self.leaf is not None:
            return str(self.leaf)
        else:
            return f'[{self.left.__str__()},{self.right.__str__()}]'

    def explode(self, d=0):
        if d >= 4 and self.leaf is None:
            # add left value
            p = self
            while p.parent is not None and p.parent.left == p:
                p = p.parent
            p = p.parent
            if p is not None:
                n = furthest_node(p.left, 'right')
                n.leaf += self.left.leaf
            # add right value
            p = self
            while p.parent is not None and p.parent.right == p:
                p = p.parent
            p = p.parent
            if p is not None:
                n = furthest_node(p.right, 'left')
                n.leaf += self.right.leaf
            # explode and replace with 0
            self.leaf = 0
            self.left, self.right = None, None
            return True
        else:
            if self.left is not None and self.left.explode(d + 1):
                return True
            if self.right is not None and self.right.explode(d + 1):
                return True
            return False

    def split(self):
        if self.leaf is not None:
            if self.leaf >= 10:
                self.left, self.right = Tree(floor(self.leaf / 2)), Tree(ceil(self.leaf / 2))
                self.left.parent, self.right.parent = self, self
                self.leaf = None
                return True
            else:
                return False
        else:
            # exploit priority of or operator
            return self.left.split() or self.right.split()

    def reduce(self):
        # exploit priority of or operator
        while self.explode() or self.split():
            pass
        return self

    def magnitude(self):
        if self.leaf is not None:
            return self.leaf
        else:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, tree):
        return Tree([self, tree]).reduce()


@aoc.pretty_solution(1)
def part1(data):
    tree = Tree(data[0])
    for i in range(1, len(data)):
        tree += Tree(data[i])
    return tree.magnitude()


@aoc.pretty_solution(2)
def part2(data):
    res = 0
    for i in range(len(data)):
        for j in range(len(data)):
            if i != j:
                res = max(res, (Tree(data[i]) + Tree(data[j])).magnitude())
    return res


def main():
    def map_line(line):
        return eval(line)

    data = aoc_parse.map_input_lines(prj_path + '/year2021/input/day18.txt', map_line)
    return part1(data), part2(data)


if __name__ == "__main__":
    main()
