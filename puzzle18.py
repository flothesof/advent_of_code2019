import networkx as nx
from frozendict import frozendict

import functools


inp1 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

inp2 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

inp3 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""


def make_coord2val(inp1):
    vault = dict()
    for r, row in enumerate(inp1.split('\n')):
        for c, val in enumerate(row):
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

@functools.lru_cache(maxsize=2**20)
def find_items_on_way(source, target, G, vault):
    s = list({k: v for k, v in vault.items() if v == source}.keys())[0]
    t = list({k: v for k, v in vault.items() if v == target}.keys())[0]
    items = []
    for coord in nx.shortest_path(G, source=s, target=t)[1:-1]:
        if vault[coord] not in '.':
            items.append(vault[coord])
    return items


def move(vault, item_to_fetch):
    current_player_pos = list({k for k, v in vault.items() if v == '@'})[0]
    item_to_fetch_pos = list({k for k, v in vault.items() if v == item_to_fetch})[0]
    new_vault = dict(vault)
    new_vault[current_player_pos] = '.'
    new_vault[item_to_fetch_pos] = '@'
    return new_vault


def compute_steps(item, G, vault):
    s = list({k: v for k, v in vault.items() if v == '@'}.keys())[0]
    t = list({k: v for k, v in vault.items() if v == item}.keys())[0]
    return len(nx.shortest_path(G, source=s, target=t)) - 1




@functools.lru_cache(maxsize=2**20)
def solve(inputs):
    steps_taken, collected_keys, vault = inputs
    G = build_graph(vault)
    needs = {}
    for item in set(item for item in vault.values() if item not in '.#@'):
        needs[item] = find_items_on_way('@', item, G, vault)
    for item in needs:
        if item in 'ABCDEFGHIJKLMNOPQRSTUVXYZ':
            if item.lower() not in collected_keys:
                needs[item].append(item.lower())
    accessible = [item for item in needs if len(needs[item]) == 0]
    # print(f"items I can get directly: {accessible}")
    if len(accessible) > 0:
        outputs = []
        for item in accessible:
            # print(f"I will fetch '{item}', replacing '@' with '{item}', taking {compute_steps(item, G, vault)} steps")
            new_collected_keys = list(collected_keys)
            if item in 'ABCDEFGHIJKLMNOPQRSTUVXYZ'.lower():
                new_collected_keys.append(item)
            new_vault = move(vault, item)
            outputs.append(solve((steps_taken + compute_steps(item, G, vault), tuple(new_collected_keys), frozendict(new_vault))))
        return min(outputs, key=lambda items: items[0])
    else:
        return steps_taken, collected_keys, vault


vault = make_coord2val(inp1)
G = build_graph(vault)
assert sorted(find_items_on_way('f', '@', G, vault)) == sorted(['D', 'E', 'e', 'C', 'b', 'A'])
steps_taken, collected_keys, new_vault = solve((0, (), frozendict(vault)))
assert steps_taken == 86

vault = make_coord2val(inp2)
steps_taken, collected_keys, new_vault = solve((0, (), frozendict(vault)))
assert steps_taken == 132


