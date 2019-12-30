from puzzle18_part1 import *

test_inp1 = """#######
#a.#Cd#
##1#2##
#######
##4#3##
#cB#.b#
#######"""

test_inp2 = """###############
#d.ABC.#.....a#
######1#2######
###############
######4#3######
#b.....#.....c#
###############"""

test_inp3 = """#############
#DcBa.#.GhKl#
#.###1#2#I###
#e#d#####j#k#
###C#4#3###J#
#fEbA.#.FgHi#
#############"""

test_inp4 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba1#2BcIJ#
#############
#nK.L4#3G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

inp = open('data/input18_part2').read().strip()


def static_shortest_paths(vault):
    symbols = set(val for val in set(vault.values()) if val != '.')
    symbol2pos = {v: k for k, v in vault.items()}
    G = build_graph(vault)
    shortest_paths = dict()
    for first in symbols:
        shortest_paths[first] = {}
        for second in symbols:
            if first != second:
                try:
                    shortest_paths[first][second] = len(nx.shortest_path(G, symbol2pos[first], symbol2pos[second])) - 1
                except nx.NetworkXNoPath:
                    pass
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
                try:
                    path = nx.shortest_path(G, symbol2pos[first], symbol2pos[second])
                    items = []
                    for coord in path:
                        if vault[coord] not in '.@1234':
                            items.append(vault[coord])
                    items_on_way[first][second] = items
                except nx.NetworkXNoPath:
                    pass

    return items_on_way


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


vault = make_coord2val(test_inp1)
shortest_paths = static_shortest_paths(vault)
items_on_way = static_items_on_way(vault)
keys = set([val for val in set(vault.values()) if val in alphabet])


# part2
@lru_cache(maxsize=2 ** 20)
def minsteps_part2(current_positions, n_keys_to_find, current_keys):
    if n_keys_to_find == 0:
        return 0

    best = INFINITY
    for current_pos in current_positions:
        for new_key in next_possible_keys(items_on_way, current_pos, current_keys):
            new_keys = current_keys.union({new_key})
            dist = shortest_paths[current_pos][new_key]
            new_positions = current_positions.replace(current_pos, new_key)
            dist += minsteps_part2(new_positions, n_keys_to_find - 1, new_keys)

            if dist < best:
                best = dist

    return best


# test cases
for test_inp, expected in zip([test_inp1, test_inp2, test_inp3, test_inp4],
                              [8, 24, 32, 72]):
    vault = make_coord2val(test_inp)
    shortest_paths = static_shortest_paths(vault)
    items_on_way = static_items_on_way(vault)
    keys = set([val for val in set(vault.values()) if val in alphabet])
    # beware: to pass the test cases we need to clear our cache...
    minsteps_part2.cache_clear()
    mini = minsteps_part2('1234', len(keys), current_keys=frozenset())
    assert mini == expected

vault = make_coord2val(inp)
shortest_paths = static_shortest_paths(vault)
items_on_way = static_items_on_way(vault)
keys = set([val for val in set(vault.values()) if val in alphabet])
minsteps_part2.cache_clear()
mini = minsteps_part2('1234', len(keys), current_keys=frozenset())
print(f'solution for part2: {mini}')
