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


def run(input_program, input_values):
    program = input_program[:]
    index = 0
    relative_base = 0
    extra_mem = {}
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
            input_value = input_values.pop()
            write(program, write_addr, input_value, extra_mem)
            index += nincrement
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
    return program, prints


assert run([1002, 4, 3, 4, 33], input_values=[1])[0] == [1002, 4, 3, 4, 99]
assert run([1101, 100, -1, 4, 0], input_values=[1])[0] == [1101, 100, -1, 4, 99]
program = list(map(int, open('data/input05').read().split(',')))
assert run(program, input_values=[1])[1][-1] == 6731945
assert run(program, input_values=[5])[1][-1] == 9571668
# unit tests puzzle05
assert run([1002, 4, 3, 4, 33], input_values=[1])[0] == [1002, 4, 3, 4, 99]
assert run([1101, 100, -1, 4, 0], input_values=[1])[0] == [1101, 100, -1, 4, 99]
assert run([3, 0, 4, 0, 99], input_values=[2])[1] == [2]
program = list(map(int, open('data/input05').read().split(',')))
assert run(program, input_values=[1])[1][-1] == 6731945

# unit tests part1
expected1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16,
             101, 1006, 101, 0, 99]
assert run([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99], input_values=[1])[1] == expected1
n = run([1102, 34915192, 34915192, 7, 4, 7, 99, 0], input_values=[1])[1][0]
assert len(str(n)) == 16
assert run([104, 1125899906842624, 99], input_values=[1])[1][0] == 1125899906842624

print('all tests running')
program = list(map(int, open('data/input09').read().split(',')))
_, prints = run(program, input_values=[1])
print(f'solution for part1: {prints[0]}')
_, prints = run(program, input_values=[2])
print(f'solution for part2: {prints[0]}')