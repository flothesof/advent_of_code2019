base_vectors = {'R': 1 + 0j,
                'L': -1 + 0j,
                'U': 0 + 1j,
                'D': 0 - 1j}


def decode(wire):
    points = [0 + 0j]
    for segment in wire.split(','):
        direction, length = segment[0], int(segment[1:])
        start = points[-1]
        new_points = [start + l * base_vectors[direction] for l in range(1, length + 1)]
        points.extend(new_points)
    return points


def manhattan_dist(c):
    return abs(c.real) + abs(c.imag)


def compute_distance(wire1, wire2):
    points1 = decode(wire1)
    points2 = decode(wire2)
    common_points = set(points1).intersection(set(points2))
    common_points.remove(points1[0])
    return min(manhattan_dist(c) for c in common_points)


def unit_tests():
    wire1 = 'R8,U5,L5,D3'
    wire2 = 'U7,R6,D4,L4'
    assert compute_distance(wire1, wire2) == 6.
    wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    assert compute_distance(wire1, wire2) == 159.
    wire1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    wire2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    assert compute_distance(wire1, wire2) == 135.
    return True


if __name__ == '__main__':
    print(f'unit tests pass: {unit_tests()}')
    wire1, wire2 = open('data/input03').readlines()
    wire1 = wire1.strip()
    wire2 = wire2.strip()
    print(f'solution to part1: {compute_distance(wire1, wire2)}')
