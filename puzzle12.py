import numpy as np

inp1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""


def parse_input(inp1):
    lines = inp1.split('\n')
    moons = []
    for line in lines:
        coords = line.split(',')
        moon = []
        for coord in coords:
            coord = coord.replace(' ', '').replace('<', '').replace('>', '')
            moon.append(int(coord.split('=')[1]))
        moons.append(np.array(moon))
    return dict(zip(['Io', 'Europa', 'Ganymede', 'Callisto'], moons))


# moons 'Io', 'Europa', 'Ganymede', 'Callisto'
def step(moons, velocities):
    # update velocities
    for moon in moons:
        x1 = moons[moon]
        v1 = velocities[moon]
        for other_moon in moons:
            if moon != other_moon:
                x2 = moons[other_moon]
                dx = x2 - x1
                v1 += np.sign(dx)
    # update positions
    for moon in moons:
        x1 = moons[moon]
        v1 = velocities[moon]
        x1 += v1
    return moons, velocities


def printout(step, moons, velocities):
    print(f'after {step} steps')
    for moon in moons:
        pos = moons[moon]
        vel = velocities[moon]
        print(f'pos=<x={pos[0]}, y={pos[1]}, z={pos[2]}>, vel=<x={vel[0]}, y={vel[1]}, z={vel[2]}>')
    print(f'total energy: {total_energy(moons, velocities)}')


def total_energy(moons, velocities):
    total = []
    for moon in moons:
        pot = np.sum(np.abs(moons[moon]))
        kin = np.sum(np.abs(velocities[moon]))
        total.append(pot * kin)
    return sum(total)


# unit test part1
moons = parse_input(inp1)
assert np.allclose(moons['Io'], np.array([-1, 0, 2]))
velocities = {key: np.array([0, 0, 0]) for key in moons}
if False:
    printout(0, moons, velocities)
    moons, velocities = step(moons, velocities)
    printout(1, moons, velocities)
    for _ in range(9):
        moons, velocities = step(moons, velocities)
    printout(10, moons, velocities)
    assert total_energy(moons, velocities) == 179

# part1
moons = parse_input(open('data/input12').read().strip())
velocities = {key: np.array([0, 0, 0]) for key in moons}
for _ in range(1000):
    moons, velocities = step(moons, velocities)
print(f'solution for part1: {total_energy(moons, velocities)}')


def hash(moons, velocities):
    return "".join(map(str, np.array(list(moons.values()) + list(velocities.values())).ravel().tolist()))


def get_cycle(moons, coordinate_index):
    """Finds a cycle in coordinate x1 only by simulating x1 = f(x1, vx1)."""
    moons = {key: moons[key][coordinate_index + 0:coordinate_index + 1] for key in moons}
    velocities = {key: np.array([0]) for key in moons}
    initial_hash = hash(moons, velocities)
    nsteps = 0
    while True:
        moons, velocities = step(moons, velocities)
        nsteps += 1
        curr_hash = hash(moons, velocities)
        if curr_hash == initial_hash:
            break
    return nsteps


# part2 unit test
moons = parse_input(inp1)
period0 = get_cycle(moons, coordinate_index=0)
period1 = get_cycle(moons, coordinate_index=1)
period2 = get_cycle(moons, coordinate_index=2)
min_cycle = min(np.lcm(np.lcm(period0, period1), period2), np.lcm(np.lcm(period0, period2), period1),
                np.lcm(np.lcm(period1, period2), period0))
assert min_cycle == 2772

# part2
moons = parse_input(open('data/input12').read().strip())
period0 = get_cycle(moons, coordinate_index=0)
period1 = get_cycle(moons, coordinate_index=1)
period2 = get_cycle(moons, coordinate_index=2)
min_cycle = min(np.lcm(np.lcm(period0, period1), period2), np.lcm(np.lcm(period0, period2), period1),
                np.lcm(np.lcm(period1, period2), period0))
print(f"solution for part2: {min_cycle}")
