from advent_of_code.lib.import_all import *
import networkx as nx


def get_input(file):
    raw = aoc.read_input(2023, 25, file)
    graph = defaultdict(set)
    for line in aoc_parse.as_lines(raw):
        node, *edges = line.replace(":","").split()
        for edge in edges:
            graph[node].add(edge)
            graph[edge].add(node)
    return graph


@aoc.pretty_solution(1)
def part1(graph):
    # saw this approach on reddit
    # making heavy use of external library networkx

    # create networkx graph object
    kx_graph = nx.Graph()
    for node, edges in graph.items():
        for edge in edges:
            kx_graph.add_edge(node, edge)

    remove = nx.minimum_edge_cut(kx_graph)
    for a, b in remove:
        kx_graph.remove_edge(a, b)

    return prod(map(len, nx.connected_components(kx_graph)))


def main():
    data = get_input("example.txt")
    part1(data)


def test():
    data = get_input("input.txt")
    assert part1(data) == 555856
    print("Test OK")


if __name__ == "__main__":
    test()
