import json
from collections import Counter
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
    graph = graph.subgraph(nodes)
    result = {}
    for node in nodes:
        neighbors = list(graph.neighbors(node))
        # if len(neighbors) == 1:
        #     continue
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
