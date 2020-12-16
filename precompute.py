import json
from collections import Counter, defaultdict
from itertools import combinations

import networkx
import requests
from littleutils import group_by_key_func
from networkx import Graph

from common import DATA_PATH


def precompute(words, length):
    words = [w for w in words if len(w) == length]
    by_letters = group_by_key_func(words, lambda w: "".join(sorted(w)))

    graph = Graph()
    by_subletters = defaultdict(list)
    for key in by_letters:
        counts = tuple(Counter(key).items())
        for differing_letters in [1, 2]:
            for subletters in combinations(counts, len(counts) - differing_letters):
                by_subletters[subletters].append(key)

    for group in by_subletters.values():
        for u, v in combinations(group, 2):
            u_counts = Counter(u)
            v_counts = Counter(v)
            less = None
            more = None
            for letter in u_counts.keys() | v_counts.keys():
                if u_counts[letter] == v_counts[letter]:
                    continue
                elif u_counts[letter] == v_counts[letter] + 1 and more is None:
                    more = letter
                elif u_counts[letter] == v_counts[letter] - 1 and less is None:
                    less = letter
                else:
                    break
            else:
                assert less and more
                graph.add_edge(u, v)

    components = list(networkx.connected_components(graph))
    nodes = list(max(components, key=len))
    graph: networkx.Graph = graph.subgraph(nodes).copy()
    degree = graph.degree
    leaves = [node for node in nodes if degree[node] == 1]
    for leaf in leaves:
        while True:
            neighbors = list(graph.neighbors(leaf))
            if len(neighbors) != 1:
                break
            graph.remove_node(leaf)
            leaf = neighbors[0]

    result = {}
    for node in graph:
        neighbors = list(graph.neighbors(node))
        assert len(neighbors) > 1
        result[node] = [by_letters[node], neighbors]
    return result


def precompute_all():
    words = requests.get("http://www.mieliestronk.com/corncob_lowercase.txt").text.split()
    result = {}
    for length in range(8, 9):
        print(f"Precomputing length {length}")
        result[length] = precompute(words, length)

    DATA_PATH.write_text(json.dumps(result))


precompute_all()
