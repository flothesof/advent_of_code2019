"""Source code for my resumable intcode computer."""

from enum import IntEnum


class IntCodeStatus(IntEnum):
    WAITING_FOR_INPUT = 1
    TERMINATED = 2


def write(program, pos, value, extra_mem):
    if is_valid(pos, program):
        program[pos] = value
    else:
        extra_mem[pos] = value


def is_valid(addr, program):
    return 0 <= addr < len(program)


def load_param(program, pos, mode_param, extra_mem, relative_base):
    if mode_param == '0':  # position
        addr = program[pos]
        if is_valid(addr, program):
            param = program[addr]
        else:
            if addr in extra_mem:
                param = extra_mem[addr]
            else:
                extra_mem[addr] = 0
                param = 0
    elif mode_param == '1':  # immediate
        param = program[pos]
    elif mode_param == '2':  # relative
        addr = relative_base + program[pos]
        if is_valid(addr, program):
            param = program[addr]
        else:
            if addr in extra_mem:
                param = extra_mem[addr]
            else:
                extra_mem[addr] = 0
                param = 0
    else:
        raise NotImplementedError
    return param


def load_addr(program, pos, mode_param, relative_base):
    if mode_param == '0':
        addr = program[pos]
    elif mode_param == '1':
        addr = pos
    elif mode_param == '2':
        addr = relative_base + program[pos]
    else:
        raise NotImplementedError
    return addr


class IntCodeComputer:
    def __init__(self, input_program, resume):
        self.input_program = input_program
        self.resume = resume
        self.state = None

    def restore_state(self):
        if self.state is None:
            raise ValueError
        else:
            return self.state

    def save_state(self, program, index, relative_base, extra_mem, prints):
        self.state = program[:], index, relative_base, extra_mem.copy(), prints[:]

    def run(self, input_values):
        if not self.resume:
            program = self.input_program[:]
            index = 0
            relative_base = 0
            extra_mem = {}
            prints = []
        else:
            if self.state is None:
                program = self.input_program[:]
                index = 0
                relative_base = 0
                extra_mem = {}
                prints = []
            else:
                program, index, relative_base, extra_mem, prints = self.restore_state()
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
                    input_value = input_values.pop(0)
                    write(program, write_addr, input_value, extra_mem)
                    index += nincrement
                else:
                    self.save_state(program, index, relative_base, extra_mem, prints)
                    return program, prints, IntCodeStatus.WAITING_FOR_INPUT
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
                return program, prints, IntCodeStatus.TERMINATED
            else:
                raise NotImplementedError()


# unit tests puzzle05
assert IntCodeComputer([1002, 4, 3, 4, 33], resume=False).run([1])[0] == [1002, 4, 3, 4, 99]
assert IntCodeComputer([1101, 100, -1, 4, 0], resume=False).run([1])[0] == [1101, 100, -1, 4, 99]
program = list(map(int, open('data/input05').read().split(',')))
assert IntCodeComputer(program, resume=False).run(input_values=[1])[1][-1] == 6731945
assert IntCodeComputer(program, resume=False).run(input_values=[5])[1][-1] == 9571668


# tests from Day 11: Space Police
def move_robot(program, robot_pos=0 + 0j, robot_dir=1j, hull=None):
    if hull is None:
        hull = {}
    painted_panels = {}
    intcode = IntCodeComputer(program, resume=True)
    while True:
        current_paint = get_value(hull, robot_pos)
        program, prints, status = intcode.run([current_paint])
        if status == IntCodeStatus.WAITING_FOR_INPUT:
            assert len(prints) >= 2
            color, rotation = prints[-2:]
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


program = list(map(int, open('data/input11').read().split(',')))


def get_value(hull, pos):
    if pos in hull:
        return hull[pos]
    else:
        return 0  # everything starts black


def write_value(hull, pos, value):
    hull[pos] = value


painted_panels, hull = move_robot(program)
assert len(painted_panels) == 2441

print('all tests passed')
