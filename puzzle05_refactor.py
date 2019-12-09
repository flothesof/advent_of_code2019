def load_param(program, pos, mode_param):
    if mode_param == '0':  # position
        param = program[program[pos]]
    elif mode_param == '1':  # immediate
        param = program[pos]
    else:
        raise NotImplementedError
    return param


def load_addr(program, pos, mode_param):
    if mode_param == '0':
        addr = program[pos]
    elif mode_param == '1':
        addr = pos
    else:
        raise NotImplementedError
    return addr


def run(input_program, input_values):
    program = input_program[:]
    index = 0
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
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            assert mode_param3 == '0'
            write_addr = program[index + 3]
            program[write_addr] = param1 + param2
            index += nincrement
        # multiply
        elif op == '02':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            assert mode_param3 == '0'
            write_addr = program[index + 3]
            program[write_addr] = param1 * param2
            index += nincrement
        # input_value written to address
        elif op == '03':
            nincrement = 2
            assert mode_param1 == '0'
            write_addr = program[index + 1]
            input_value = input_values.pop()
            program[write_addr] = input_value
            index += nincrement
        # output parameter
        elif op == '04':
            nincrement = 2
            addr = load_addr(program, index + 1, mode_param1)
            prints.append(program[addr])
            index += nincrement
        # jump if true
        elif op == '05':
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            if param1 != 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # jump if false
        elif op == '06':
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            if param1 == 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # less than
        elif op == '07':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            assert mode_param3 == '0'
            write_addr = load_addr(program, index + 3, mode_param3)
            if param1 < param2:  # strict?
                program[write_addr] = 1
            else:
                program[write_addr] = 0
            index += nincrement
        # equals
        elif op == '08':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1)
            param2 = load_param(program, index + 2, mode_param2)
            assert mode_param3 == '0'
            write_addr = load_addr(program, index + 3, mode_param3)
            if param1 == param2:
                program[write_addr] = 1
            else:
                program[write_addr] = 0
            index += nincrement
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
print('all tests running')
