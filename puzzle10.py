from math import atan2, pi
import matplotlib.pyplot as plt
import matplotlib as mpl

EPS = 0.000001

astmap = """.#..#
.....
#####
....#
...##"""

astmap1 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""

astmap2 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""

astmap3 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""


def map2xy(astmap, ast='#'):
    asteroids = []
    for y, row in enumerate(astmap.split('\n')):
        for x, val in enumerate(row):
            if val == ast:
                asteroids.append(x - 1j * y)
    return asteroids


def compute_angles(ast, asteroids):
    data = []
    for other_ast in asteroids:
        if other_ast != ast:
            direction = other_ast - ast
            length = abs(direction)
            direction = direction / length
            data.append((length, direction, other_ast))
    data = sorted(data, key=lambda items: items[0])
    return data


def detected(ast, asteroids, eps=EPS):
    detection_dirs = {}
    for length, dir, other_ast in compute_angles(ast, asteroids):
        if len(detection_dirs) == 0:
            detection_dirs[dir] = other_ast
        elif min([abs(dir - other_dir) for other_dir in detection_dirs]) > eps:
            detection_dirs[dir] = other_ast
    return len(detection_dirs), list(detection_dirs.values())


# unit tests
asteroids = map2xy(astmap)
assert [detected(ast, asteroids)[0] for ast in asteroids] == [7, 7, 6, 7, 7, 7, 5, 7, 8, 7]
asteroids = map2xy(astmap1)
assert max(detected(ast, asteroids)[0] for ast in asteroids) == 33
asteroids = map2xy(astmap2)
assert max(detected(ast, asteroids)[0] for ast in asteroids) == 41
asteroids = map2xy(astmap3)
assert max(detected(ast, asteroids)[0] for ast in asteroids) == 210

# part1
asteroids = map2xy(open('data/input10').read())
mapping = [(ast, detected(ast, asteroids)[0]) for ast in asteroids]
print(f'solution for part1: {max(mapping, key=lambda items: items[1])[1]}')


# part2
def angle(center_ast, ast, eps=EPS):
    dz = ast - center_ast
    return -(atan2(dz.imag, dz.real) - (pi / 2 + eps)) % (2 * pi)


assert sorted([1, 1 + 1j, 1j, -1 - 1j], key=lambda item: angle(0 + 0j, item)) == [1j, 1 + 1j, 1, -1 - 1j]

# part2
ast = max(mapping, key=lambda items: items[1])[0]  # (22+28j)
assert ast == 22 - 28j
current_angle = 0
vaporized = []
vaporized_angles = []
while True:
    #print(f'len(asteroids)={len(asteroids)}')
    data = compute_angles(ast, asteroids)
    _, seen_asts = detected(ast, asteroids)
    angles = [angle(ast, other_ast) for other_ast in seen_asts]
    sorted_asts = sorted(seen_asts, key=lambda other_ast: angle(ast, other_ast))
    for to_vaporize in sorted_asts:
        new_angle = angle(ast, to_vaporize)
        if new_angle > current_angle:
            current_angle = new_angle
            asteroids.remove(to_vaporize)
            vaporized.append(to_vaporize)
            vaporized_angles.append(new_angle)
            break
    if len(vaporized) == 200:
        break

# 2127 too high
# 2017 too high
# 1700 too high
# 1823 not right
# 0 not right
# 1577 not right
part2 = vaporized[-1]
print(f"solution for part2: {100 * part2.real - part2.imag}")


# debugging plots
def plot_asts(center_ast, seen_asts, coloring=None):
    x = [ast.real for ast in seen_asts]
    y = [ast.imag for ast in seen_asts]
    x0, y0 = center_ast.real, center_ast.imag
    fig, ax = plt.subplots()
    # lines of sight
    if coloring is None:
        for xx, yy in zip(x, y):
            ax.plot([x0, xx], [y0, yy], 'grey', alpha=0.2)
    else:
        assert len(coloring) == len(seen_asts)
        mini, maxi = min(coloring), max(coloring)
        assert maxi > mini
        cmap = plt.get_cmap('Reds')
        for xx, yy, cval in zip(x, y, coloring):
            color = cmap((cval - mini) / (maxi - mini))
            ax.plot([x0, xx], [y0, yy], color=color, alpha=0.8)
    # asteroids
    ax.plot(x, y, 'bo')
    ax.plot(x0, y0, 'ro')
    ax.axis('equal')
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm)
    return ax


ax = plot_asts(ast, seen_asts, coloring=angles)
x = [ast.real for ast in vaporized]
y = [ast.imag for ast in vaporized]
ax.plot(x, y, '-o', lw=2)
plt.show()
