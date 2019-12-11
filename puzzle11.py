from puzzle09 import write, load_param, load_addr, is_valid


def run(input_program, input_values, index=0, relative_base=0, extra_mem=None):
    if extra_mem is None:
        extra_mem = {}
    program = input_program[:]

    prints = []
    while True:
        instruction = program[index]
        op_str = f"{instruction:05}"  # pad with zeros if necessary
        op = op_str[-2:]
        mode_param3, mode_param2, mode_param1 = op_str[0], op_str[1], op_str[2]
        jump = False
        # add
        if op == '01':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            write(program, write_addr, param1 + param2, extra_mem)
            index += nincrement
        # multiply
        elif op == '02':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            write(program, write_addr, param1 * param2, extra_mem)
            index += nincrement
        # input_value written to address
        elif op == '03':
            nincrement = 2
            write_addr = load_addr(program, index + 1, mode_param1, relative_base)
            if len(input_values) > 0:
                input_value = input_values.pop()
                write(program, write_addr, input_value, extra_mem)
                index += nincrement
            else:
                return program, prints, index, extra_mem, relative_base, False

        # output parameter
        elif op == '04':
            nincrement = 2
            addr = load_addr(program, index + 1, mode_param1, relative_base)
            if is_valid(addr, program):
                prints.append(program[addr])
            elif addr in extra_mem:
                prints.append(extra_mem[addr])
            else:
                raise ValueError
            index += nincrement
        # jump if true
        elif op == '05':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            if param1 != 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # jump if false
        elif op == '06':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            if param1 == 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # less than
        elif op == '07':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            if param1 < param2:  # strict?
                write(program, write_addr, 1, extra_mem)
            else:
                write(program, write_addr, 0, extra_mem)
            index += nincrement
        # equals
        elif op == '08':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            if param1 == param2:
                write(program, write_addr, 1, extra_mem)
            else:
                write(program, write_addr, 0, extra_mem)
            index += nincrement
        # adjust relative base
        elif op == '09':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            relative_base += param1
            index += 2
        # end program
        elif op == '99':
            break
        else:
            raise NotImplementedError()
    return program, prints, index, extra_mem, relative_base, True


program = list(map(int, open('data/input11').read().split(',')))


def get_value(hull, pos):
    if pos in hull:
        return hull[pos]
    else:
        return 0  # everything starts black


def write_value(hull, pos, value):
    hull[pos] = value


def move_robot(program, robot_pos=0 + 0j, robot_dir=1j, hull=None):
    state = program[:]
    if hull is None:
        hull = {}
    painted_panels = {}
    index = 0
    relative_base = 0
    extra_mem = {}
    while True:
        current_paint = get_value(hull, robot_pos)
        state, prints, index, extra_mem, relative_base, finished = run(state, [current_paint], index=index,
                                                                       extra_mem=extra_mem,
                                                                       relative_base=relative_base)
        if not finished:
            assert len(prints) == 2
            color, rotation = prints
            # paint
            assert color in [0, 1]
            write_value(hull, robot_pos, color)
            if color != current_paint:
                write_value(painted_panels, robot_pos, 1)
            # turn left
            assert rotation in [0, 1]
            if rotation == 0:
                robot_dir = robot_dir * 1j
            elif rotation == 1:
                robot_dir = robot_dir * (-1j)
            robot_pos = robot_pos + robot_dir
        else:
            break
    return painted_panels, hull


# part1
painted_panels, hull = move_robot(program)
print(f'solution for part1: {len(painted_panels)}')
# part2
painted_panels, hull = move_robot(program, hull={0 + 0j: 1})
print('solution for part2: look at the image')
import numpy as np
import matplotlib.pyplot as plt

xx = [point.real for point in hull]
yy = [point.imag for point in hull]
vals = [hull[point] for point in hull]
xmin, xmax = min(xx), max(xx)
dx = int(xmax - xmin)
ymin, ymax = min(yy), max(yy)
dy = int(ymax - ymin)
hull_drawing = np.zeros((dy + 1, dx + 1))
for x, y, val in zip(xx, yy, vals):
    x = x - xmin
    y = y - ymin
    hull_drawing[int(y), int(x)] = val
plt.imshow(hull_drawing[::-1, :])
