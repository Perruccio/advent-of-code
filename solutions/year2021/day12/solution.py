import pathlib
import aoc.parse
import aoc
from collections import defaultdict, deque


def paths(graph, start, end, single_small_twice=False):
    # (node, visited, can_visit_one_small_twice)
    # define a state as the current node + the set of visited nodes,
    # so that the back-tracking is automatic. add 'twice' for part 2
    # use DFS to lower the memory used
    stack = deque([(start, {start}, single_small_twice)])

    res = 0
    while stack:
        # visit last appended state (DFS, lifo)
        node, visited, twice = stack.pop()

        # stopping condition
        if node == end:
            res += 1
            continue

        # DFS, search new states from current node
        # only look for new nodes or "big" nodes
        # (or also for only the first repetition of a "small" nodes)
        for next_node in graph[node]:
            check = next_node not in visited or next_node.isupper()
            if check or twice:
                stack.append((next_node, visited | {next_node}, twice and check))
    return res


@aoc.pretty_solution(1)
def part1(data):
    return paths(data, 'start', 'end')


@aoc.pretty_solution(2)
def part2(data):
    return paths(data, 'start', 'end', True)


def main():
    def map_line(line):
        return line.split('-')

    raw = aoc.parse.map_input_lines(str(pathlib.Path(__file__).parent/'input.txt'), map_line)

    data = defaultdict(set)
    for a, b in raw:
        # don't add links to start as they are useless and are a problem for part 2
        if b != 'start':
            data[a].add(b)
        if a != 'start':
            data[b].add(a)
    return part1(data), part2(data)
    

def test():
    p1, p2 = main()
    assert p1 == 5104
    assert p2 == 149220


if __name__ == "__main__":
    main()
