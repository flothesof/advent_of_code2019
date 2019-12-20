import networkx as nx
import re
from collections import defaultdict

test_inp1 = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """

# parsing input
nodes = set()
rows = test_inp1.split('\n')
for r, row in enumerate(rows):
    if '#' in row:
        for c, val in enumerate(row):
            if val == '.':
                nodes.add((r, c))
# building a graph of connected nodes
G = nx.Graph()
G.add_nodes_from(nodes)
for (r, c) in nodes:
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (r + dr, c + dc) in nodes:
            G.add_edge((r, c), (r + dr, c + dc))
AA = (2, 9)
ZZ = (16, 13)

assert nx.shortest_path_length(G, AA, ZZ) == 26

horizontal_matches = []
for row in rows:
    horizontal_matches.extend(re.findall('[A-Z]{2}', row))

assert all(l == len(rows[0]) for l in [len(row) for row in rows])
cols = ["".join([row[index] for row in rows]) for index in range(len(rows[0]))]
vertical_matches = []
for col in cols:
    vertical_matches.extend(re.findall('[A-Z]{2}', col))

portals = horizontal_matches + vertical_matches
assert int((len(portals) - 2) / 2 + 2) == len(set(portals))

connected_portals = []
for portal in set(portals):
    if portals.count(portal) > 1:
        connected_portals.append(portal)

start, stop = sorted(set(portals) - set(connected_portals))

portal_pos = defaultdict(list)
for r, row in enumerate(rows):
    for m in re.finditer('(\.?)([A-Z]{2})(\.?)', row):
        if m.group(1) == '.':
            c = m.span()[0]
            portal_pos[m.group(2)].append((r, c))
        elif m.group(3) == '.':
            c = m.span()[1] - 1
            portal_pos[m.group(2)].append((r, c))
        else:
            raise ValueError
for c, col in enumerate(cols):
    for m in re.finditer('(\.?)([A-Z]{2})(\.?)', col):
        if m.group(1) == '.':
            r = m.span()[0]
            portal_pos[m.group(2)].append((r, c))
        elif m.group(3) == '.':
            r = m.span()[1] - 1
            portal_pos[m.group(2)].append((r, c))
        else:
            raise ValueError

for portal, nodes in portal_pos.items():
    if len(nodes) == 2:
        G.add_edge(nodes[0], nodes[1])

assert nx.shortest_path_length(G, AA, ZZ) == 23

test_inp2 = """                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """


def solve(inp):
    # parsing input
    nodes = set()
    rows = inp.split('\n')
    for r, row in enumerate(rows):
        if '#' in row:
            for c, val in enumerate(row):
                if val == '.':
                    nodes.add((r, c))
    # building a graph of connected nodes
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for (r, c) in nodes:
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (r + dr, c + dc) in nodes:
                G.add_edge((r, c), (r + dr, c + dc))
    horizontal_matches = []
    for row in rows:
        horizontal_matches.extend(re.findall('[A-Z]{2}', row))

    assert all(l == len(rows[0]) for l in [len(row) for row in rows])
    cols = ["".join([row[index] for row in rows]) for index in range(len(rows[0]))]
    vertical_matches = []
    for col in cols:
        vertical_matches.extend(re.findall('[A-Z]{2}', col))

    portals = horizontal_matches + vertical_matches
    assert int((len(portals) - 2) / 2 + 2) == len(set(portals))

    connected_portals = []
    for portal in set(portals):
        if portals.count(portal) > 1:
            connected_portals.append(portal)

    portal_pos = defaultdict(list)
    for r, row in enumerate(rows):
        for m in re.finditer('(\.?)([A-Z]{2})(\.?)', row):
            if m.group(1) == '.':
                c = m.span()[0]
                portal_pos[m.group(2)].append((r, c))
            elif m.group(3) == '.':
                c = m.span()[1] - 1
                portal_pos[m.group(2)].append((r, c))
            else:
                raise ValueError
    for c, col in enumerate(cols):
        for m in re.finditer('(\.?)([A-Z]{2})(\.?)', col):
            if m.group(1) == '.':
                r = m.span()[0]
                portal_pos[m.group(2)].append((r, c))
            elif m.group(3) == '.':
                r = m.span()[1] - 1
                portal_pos[m.group(2)].append((r, c))
            else:
                raise ValueError

    for portal, nodes in portal_pos.items():
        if len(nodes) == 2:
            G.add_edge(nodes[0], nodes[1])

    start, stop = [portal_pos[p][0] for p in portal_pos if len(portal_pos[p]) == 1]

    return nx.shortest_path_length(G, start, stop)


assert solve(test_inp1) == 23
assert solve(test_inp2) == 58
inp = open('data/input20').read()[:-1]
print(f"solution for part1: {solve(inp)}")

# part2 let's build an explicit recursive maze until level n
# to do that we need to distinguish between interior portals (recursion level += 1) and exterior portals (recursion level -=1)

# distinguish exterior and interior
R, C = len(rows[0]), len(cols[0])
portal_pos = defaultdict(list)
for r, row in enumerate(rows):
    for m in re.finditer('(\.?)([A-Z]{2})(\.?)', row):
        exterior = False
        if m.group(1) == '.':
            c = m.span()[0]
            if m.span()[1] == R:
                exterior = True
            portal_pos[m.group(2)].append((exterior, r, c))
        elif m.group(3) == '.':
            c = m.span()[1] - 1
            if m.span()[0] == 0:
                exterior = True
            portal_pos[m.group(2)].append((exterior, r, c))
        else:
            raise ValueError
for c, col in enumerate(cols):
    for m in re.finditer('(\.?)([A-Z]{2})(\.?)', col):
        exterior = False
        if m.group(1) == '.':
            r = m.span()[0]
            if m.span()[1] == C:
                exterior = True
            portal_pos[m.group(2)].append((exterior, r, c))
        elif m.group(3) == '.':
            r = m.span()[1] - 1
            if m.span()[0] == 0:
                exterior = True
            portal_pos[m.group(2)].append((exterior, r, c))
        else:
            raise ValueError

exterior_nodes = [p for p in portal_pos if any(items[0] for items in portal_pos[p])]
interior_nodes = [p for p in portal_pos if any(not items[0] for items in portal_pos[p])]
# print(f"exterior {exterior_nodes}, interior {interior_nodes}")

# Let's build a new connected maze with all the recursion levels
recursion_levels = 1
G_recursion = nx.Graph()
for recursion in range(recursion_levels):
    nodes = set()
    rows = test_inp1.split('\n')
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            if val == '.':
                nodes.add((r, c, recursion))
    G_recursion.add_nodes_from(nodes)
    for (r, c, recursion) in nodes:
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (r + dr, c + dc, recursion) in nodes:
                G_recursion.add_edge((r, c, recursion), (r + dr, c + dc, recursion))

startstop = [p for p in portal_pos if len(portal_pos[p]) == 1]

for p in portal_pos:
    portal_pos[p] = sorted(portal_pos[p], key=lambda item: item[0])

for recursion in range(recursion_levels):
    for p in portal_pos:
        if p not in startstop:
            int_node, ext_node = portal_pos[p]
            if recursion == 0:
                # only link from interior to level + 1
                G_recursion.add_edge((int_node[1], int_node[2], recursion),
                                     (ext_node[1], ext_node[2], recursion + 1))
            elif recursion == recursion_levels - 1:
                # only link from exterior to level - 1
                G_recursion.add_edge((ext_node[1], ext_node[2], recursion),
                                     (int_node[1], int_node[2], recursion - 1))
            else:
                # link from interior to +1
                # link from exterior to -1
                G_recursion.add_edge((int_node[1], int_node[2], recursion),
                                     (ext_node[1], ext_node[2], recursion + 1))
                G_recursion.add_edge((ext_node[1], ext_node[2], recursion),
                                     (int_node[1], int_node[2], recursion - 1))

start = portal_pos[startstop[0]][0][1:] + (0,)
stop = portal_pos[startstop[1]][0][1:] + (0,)
nx.shortest_path_length(G_recursion, start, stop)

test_inp3 = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """


def solve_recursive(inp, recursion_levels=1):
    rows = inp.split('\n')
    assert all(l == len(rows[0]) for l in [len(row) for row in rows])
    cols = ["".join([row[index] for row in rows]) for index in range(len(rows[0]))]

    R, C = len(rows[0]), len(cols[0])
    #print(f"R {R}, C {C}")
    portal_pos = defaultdict(list)
    for r, row in enumerate(rows):
        for m in re.finditer('(\.?)([A-Z]{2})(\.?)', row):
            exterior = False
            if m.group(1) == '.':
                c = m.span()[0]
                if m.span()[1] == R:
                    exterior = True
                portal_pos[m.group(2)].append((exterior, r, c))
            elif m.group(3) == '.':
                c = m.span()[1] - 1
                if m.span()[0] == 0:
                    exterior = True
                portal_pos[m.group(2)].append((exterior, r, c))
            else:
                raise ValueError
    for c, col in enumerate(cols):
        for m in re.finditer('(\.?)([A-Z]{2})(\.?)', col):
            exterior = False
            if m.group(1) == '.':
                r = m.span()[0]
                if m.span()[1] == C:
                    exterior = True
                portal_pos[m.group(2)].append((exterior, r, c))
            elif m.group(3) == '.':
                r = m.span()[1] - 1
                if m.span()[0] == 0:
                    exterior = True
                portal_pos[m.group(2)].append((exterior, r, c))
            else:
                raise ValueError

    exterior_nodes = [p for p in portal_pos if any(items[0] for items in portal_pos[p])]
    interior_nodes = [p for p in portal_pos if any(not items[0] for items in portal_pos[p])]
    #print(f"exterior {exterior_nodes}, interior {interior_nodes}")

    # Let's build a new connected maze with all the recursion levels

    G_recursion = nx.Graph()
    for recursion in range(recursion_levels):
        nodes = set()
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                if val == '.':
                    nodes.add((r, c, recursion))
        G_recursion.add_nodes_from(nodes)
        for (r, c, recursion) in nodes:
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if (r + dr, c + dc, recursion) in nodes:
                    G_recursion.add_edge((r, c, recursion), (r + dr, c + dc, recursion))

    startstop = [p for p in portal_pos if len(portal_pos[p]) == 1]

    for p in portal_pos:
        portal_pos[p] = sorted(portal_pos[p], key=lambda item: item[0])

    for recursion in range(recursion_levels):
        for p in portal_pos:
            if p not in startstop:
                int_node, ext_node = portal_pos[p]
                if recursion == 0:
                    # only link from interior to level + 1
                    G_recursion.add_edge((int_node[1], int_node[2], recursion),
                                         (ext_node[1], ext_node[2], recursion + 1))
                elif recursion == recursion_levels - 1:
                    # only link from exterior to level - 1
                    G_recursion.add_edge((ext_node[1], ext_node[2], recursion),
                                         (int_node[1], int_node[2], recursion - 1))
                else:
                    # link from interior to +1
                    # link from exterior to -1
                    G_recursion.add_edge((int_node[1], int_node[2], recursion),
                                         (ext_node[1], ext_node[2], recursion + 1))
                    G_recursion.add_edge((ext_node[1], ext_node[2], recursion),
                                         (int_node[1], int_node[2], recursion - 1))

    start = portal_pos[startstop[0]][0][1:] + (0,)
    stop = portal_pos[startstop[1]][0][1:] + (0,)
    return nx.shortest_path_length(G_recursion, start, stop)


assert solve_recursive(test_inp1, recursion_levels=1) == 26
assert solve_recursive(test_inp1, recursion_levels=2) == 26
assert solve_recursive(test_inp1, recursion_levels=3) == 26
assert solve_recursive(test_inp3, recursion_levels=20) == 396
print(f"solution for part2: {solve_recursive(inp, recursion_levels=40)}")