from enum import Enum
from random import choice
from intcode import IntCodeComputer, IntCodeStatus
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def render(environment):
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for point in environment:
        xmin = min(xmin, point.real)
        xmax = max(xmax, point.real)
        ymin = min(ymin, point.imag)
        ymax = max(ymax, point.imag)
    dx = int(xmax - xmin)
    dy = int(ymax - ymin)
    arr = np.zeros((dy + 1, dx + 1))
    arr = arr * np.nan
    for point, val in environment.items():
        x, y = point.real, point.imag
        x = int(x - xmin)
        y = int(y - ymin)
        r, c = y, x
        arr[r, c] = val
    return arr


class RobotMoves(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


vectors = {RobotMoves.NORTH: 1j,
           RobotMoves.SOUTH: -1j,
           RobotMoves.WEST: -1 + 0j,
           RobotMoves.EAST: 1 + 0j}

opposite_step = {RobotMoves.NORTH: RobotMoves.SOUTH,
                 RobotMoves.SOUTH: RobotMoves.NORTH,
                 RobotMoves.WEST: RobotMoves.EAST,
                 RobotMoves.EAST: RobotMoves.WEST}


def wall_left(environment, robot_pos, robot_orient, computer):
    left_orient = robot_orient * 1j
    abs_coords_left = robot_pos + left_orient
    if abs_coords_left in environment:
        return environment[abs_coords_left] == 0
    else:
        step_left = relative2absolute[left_orient]
        program_state, prints, status = computer.run([step_left.value])
        retval = prints[-1]
        if retval == 0:
            # it was a wall
            environment[robot_pos + left_orient] = 0
            return True
        else:
            # it was not a wall, but the robot has moved so we have to move it back
            environment[robot_pos + left_orient] = retval
            get_back_step = opposite_step[step_left]
            program_state, prints, status = computer.run([get_back_step.value])
            return False


def free_in_front(environment, robot_pos, robot_orient, computer):
    abs_coords_front = robot_pos + robot_orient
    if abs_coords_front in environment:
        return environment[abs_coords_front] != 0
    else:
        step_front = relative2absolute[robot_orient]
        program_state, prints, status = computer.run([step_front.value])
        retval = prints[-1]
        if retval == 0:
            # it was a wall
            environment[robot_pos + robot_orient] = 0
            return False
        else:
            # it was not a wall, but the robot has moved so we have to move it back
            environment[robot_pos + robot_orient] = retval
            get_back_step = opposite_step[step_front]
            program_state, prints, status = computer.run([get_back_step.value])
            return True


relative2absolute = {1j: RobotMoves.NORTH,
                     -1: RobotMoves.WEST,
                     -1j: RobotMoves.SOUTH,
                     1: RobotMoves.EAST}

DEBUG = False
program = list(map(int, open('data/input15').read().split(',')))
computer = IntCodeComputer(program, resume=True)
robot_pos = 0 + 0j
robot_orient = 1j
environment = {robot_pos: 1}
for nstep in range(10000):
    if DEBUG: print(f" ### starting: pos: {robot_pos}, orient: {robot_orient} ")
    if environment[robot_pos] == 2:
        if DEBUG: print(f"I've found something after {nstep} steps.")
        break
    else:
        if wall_left(environment, robot_pos, robot_orient, computer):
            if DEBUG: print(f"there's a wall left")
            if free_in_front(environment, robot_pos, robot_orient, computer):
                if DEBUG: print(f"it's free in front, I'm moving forward")
                step_forward = relative2absolute[robot_orient]
                program_state, prints, status = computer.run([step_forward.value])
                retval = prints[-1]
                assert retval != 0
                robot_pos = robot_pos + vectors[step_forward]
                environment[robot_pos] = retval
            else:
                if DEBUG: print(f"I have to rotate right")
                robot_orient = robot_orient * -1j
        else:
            if DEBUG: print(f"I will rotate left and move forward")
            # rotate left and move forward
            robot_orient = robot_orient * 1j
            step_forward = relative2absolute[robot_orient]
            program_state, prints, status = computer.run([step_forward.value])
            retval = prints[-1]
            assert retval != 0
            robot_pos = robot_pos + vectors[step_forward]
            environment[robot_pos] = retval

if DEBUG:
    environment[0 + 0j] = 3
    plt.close()
    fig = plt.figure()
    plt.imshow(render(environment), origin='lower')
    plt.colorbar()
    plt.show()


def build_graph(environment):
    G = nx.Graph()
    for coord, blockval in environment.items():
        if blockval != 0:
            G.add_node(coord)
    for node in G:
        for direction in [1, 1j, -1, -1j]:
            other = node + direction
            if other in G:
                G.add_edge(node, other)
    return G


G = build_graph(environment)
source = 0 + 0j
target = robot_pos
print(f"solution for part1: {nx.shortest_path_length(G, source, target)}")

# part2: let's first get a complete map of the environment by exploring it enough
for nstep in range(5000):
    if wall_left(environment, robot_pos, robot_orient, computer):
        if free_in_front(environment, robot_pos, robot_orient, computer):
            step_forward = relative2absolute[robot_orient]
            program_state, prints, status = computer.run([step_forward.value])
            retval = prints[-1]
            assert retval != 0
            robot_pos = robot_pos + vectors[step_forward]
            environment[robot_pos] = retval
        else:
            robot_orient = robot_orient * -1j
    else:
        # rotate left and move forward
        robot_orient = robot_orient * 1j
        step_forward = relative2absolute[robot_orient]
        program_state, prints, status = computer.run([step_forward.value])
        retval = prints[-1]
        assert retval != 0
        robot_pos = robot_pos + vectors[step_forward]
        environment[robot_pos] = retval

if DEBUG:
    environment[0 + 0j] = 1
    plt.close()
    fig = plt.figure()
    plt.imshow(render(environment), origin='lower')
    plt.colorbar()
    plt.show()

# part2: array based solution
G = build_graph(environment)
tmax = max(nx.shortest_path_length(G, target, other) for other in environment if environment[other] == 1)
print(f"solution for part2: {tmax}")
