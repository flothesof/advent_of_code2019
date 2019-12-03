from puzzle03 import manhattan_dist, decode


def compute_distance_with_steps(wire1, wire2):
    points1 = decode(wire1)
    steps1 = list(range(len(points1)))
    d1 = dict(zip(points1, steps1))
    points2 = decode(wire2)
    steps2 = list(range(len(points2)))
    d2 = dict(zip(points2, steps2))
    common_points = set(points1).intersection(set(points2))
    common_points.remove(points1[0])
    return min(d1[c] + d2[c] for c in common_points)


def unit_tests_part2():
    wire1 = 'R8,U5,L5,D3'
    wire2 = 'U7,R6,D4,L4'
    assert compute_distance_with_steps(wire1, wire2) == 30
    wire1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    wire2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    assert compute_distance_with_steps(wire1, wire2) == 610
    wire1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    wire2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    assert compute_distance_with_steps(wire1, wire2) == 410
    return True


print(f'unit tests pass: {unit_tests_part2()}')
wire1, wire2 = open('data/input03').readlines()
wire1 = wire1.strip()
wire2 = wire2.strip()
print(f'solution to part2: {compute_distance_with_steps(wire1, wire2)}')
