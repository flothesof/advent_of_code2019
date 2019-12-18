import networkx as nx

inp1 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

def make_coord2val(inp1):
    vault = dict()
    for r, row in enumerate(inp1.split('\n')):
        for c, val in enumerate(row):
            vault[c + 1j * r] = val
    return vault

vault = make_coord2val(inp1)

G = nx.Graph()
for coord, val in vault.items():
    if val not in '#':
        G.add_node(coord, label=val)

