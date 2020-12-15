import json
from collections import Counter

import networkx
from itertools import combinations
from littleutils import file_to_string, group_by_key_func
from networkx import Graph


def precompute(words, length):
    words = [w for w in words if len(w) == length]
    by_letters = group_by_key_func(words, lambda w: "".join(sorted(w)))

    graph = Graph()
    graph.add_nodes_from(by_letters)
    for u, v in combinations(by_letters, 2):
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

    return {node: [by_letters[node], list(graph.neighbors(node))] for node in nodes}


def precompute_all():
    words = file_to_string("/home/alex/Downloads/corncob_lowercase.txt").split()
    result = {}
    for length in range(6, 7):
        result[length] = precompute(words, length)

    with open("/tmp/word_data.json", "w") as f:
        json.dump(result, f)


precompute_all()
