inp = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".split('\n')


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = list()

    def __repr__(self):
        return f"Node {self.name}, parent: {self.parent is not None}, children: {''.join([c.name for c in self.children])}"


def build_solar_system(inp):
    nodes = {}
    for line in inp:
        sun, sat = line.split(')')
        if sun not in nodes:
            nodes[sun] = Node(sun)
        sun_node = nodes[sun]
        if sat not in nodes:
            nodes[sat] = Node(sat)
        sat_node = nodes[sat]
        sun_node.children.append(sat_node)
        sat_node.parent = sun_node
    return nodes


def count_orbits(nodes, node_name):
    node = nodes[node_name]
    orbits = 0
    if node.name == 'COM':
        return 0
    while node.parent.name != 'COM':
        orbits += 1
        node = node.parent
    return orbits + 1


# tests for part1
nodes = build_solar_system(inp)
assert count_orbits(nodes, 'D') == 3
assert count_orbits(nodes, 'L') == 7
assert count_orbits(nodes, 'COM') == 0
assert sum(map(lambda node_name: count_orbits(nodes, node_name), nodes.keys())) == 42

inp = list(map(str.strip, open('data/input06').readlines()))
nodes = build_solar_system(inp)
print(f"solution for part1: {sum(map(lambda node_name: count_orbits(nodes, node_name), nodes.keys()))}")


# part2
def get_parents(nodes, start_name):
    node = nodes[start_name]
    parents = []
    if node.name == 'COM':
        return []
    while node.parent.name != 'COM':
        node = node.parent
        parents.append(node.name)
    return parents


path_YOU = get_parents(nodes, 'YOU')
path_SAN = get_parents(nodes, 'SAN')
common_nodes = [n for n in path_YOU if n in path_SAN]
link_node = common_nodes[0]
print(f"solution for part2: {path_YOU.index(link_node) + path_SAN.index(link_node)}")
