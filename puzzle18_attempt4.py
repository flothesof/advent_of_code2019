import networkx as nx
from math import inf as INFINITY
from functools import lru_cache

test_inp1 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

test_inp2 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

test_inp3 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

test_inp4 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

inp = open('data/input18').read().strip()


def make_coord2val(inp1):
    vault = dict()
    for r, row in enumerate(inp1.split('\n')):
        for c, val in enumerate(row):
            if val not in '#':
                vault[c + 1j * r] = val
    return vault


def build_graph(vault):
    G = nx.Graph()
    for coord, val in vault.items():
        if val not in '#':
            G.add_node(coord, label=val)

    for node in G:
        for direction in [1j, -1j, 1, -1]:
            other = node + direction
            if other in G:
                G.add_edge(node, other)
    return G


def next_possible_keys(items_on_way, current_pos, current_keys):
    reachable = []
    for destination, items in items_on_way[current_pos].items():
        is_in_reach = True
        for item in items:
            if item in ALPHABET:
                if item.lower() not in current_keys:
                    is_in_reach = False
                    break
            else:
                if item != destination:
                    if item not in current_keys:
                        is_in_reach = False
                        break
        if is_in_reach and destination in keys and destination not in current_keys:
            reachable.append(destination)
    return reachable


def static_shortest_paths(vault):
    symbols = set(val for val in set(vault.values()) if val != '.')
    symbol2pos = {v: k for k, v in vault.items()}
    G = build_graph(vault)
    shortest_paths = dict()
    for first in symbols:
        shortest_paths[first] = {}
        for second in symbols:
            if first != second:
                shortest_paths[first][second] = len(nx.shortest_path(G, symbol2pos[first], symbol2pos[second])) - 1
    return shortest_paths


def static_items_on_way(vault):
    symbols = set(val for val in set(vault.values()) if val != '.')
    symbol2pos = {v: k for k, v in vault.items()}
    G = build_graph(vault)
    items_on_way = dict()
    for first in symbols:
        items_on_way[first] = {}
        for second in symbols:
            if first != second:
                path = nx.shortest_path(G, symbol2pos[first], symbol2pos[second])
                items = []
                for coord in path:
                    if vault[coord] not in '.@':
                        items.append(vault[coord])
                items_on_way[first][second] = items
    return items_on_way


ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
alphabet = ALPHABET.lower()


@lru_cache(maxsize=2 ** 20)
def minsteps(current_pos, n_keys_to_find, current_keys):
    if n_keys_to_find == 0:
        return 0

    best = INFINITY

    for new_key in next_possible_keys(items_on_way, current_pos, current_keys):
        new_keys = current_keys.union({new_key})
        dist = shortest_paths[current_pos][new_key]
        dist += minsteps(new_key, n_keys_to_find - 1, new_keys)

        if dist < best:
            best = dist

    return best


# test cases
for test_inp, expected in zip([test_inp1, test_inp2, test_inp3, test_inp4],
                              [86, 132, 136, 81]):
    vault = make_coord2val(test_inp)
    shortest_paths = static_shortest_paths(vault)
    items_on_way = static_items_on_way(vault)
    keys = set([val for val in set(vault.values()) if val in alphabet])
    mini = minsteps('@', len(keys), current_keys=frozenset())
    assert mini == expected

# part1
vault = make_coord2val(inp)
shortest_paths = static_shortest_paths(vault)
items_on_way = static_items_on_way(vault)
keys = set([val for val in set(vault.values()) if val in alphabet])
mini = minsteps('@', len(keys), current_keys=frozenset())
print(f"solution for part1: {mini}")
