def run(program, input_value):
    index = 0
    prints = []
    while True:
        instruction = program[index]
        op_str = f"{instruction:05}"  # pad with zeros if necessary
        op = op_str[-2:]
        A, B, C = op_str[0], op_str[1], op_str[2]
        jump = False
        # add
        if op == '01':
            nincrement = 4
            if C == '0':
                first = program[program[index + 1]]
            else:
                first = program[index + 1]
            if B == '0':
                second = program[program[index + 2]]
            else:
                second = program[index + 2]
            assert A == '0'
            program[program[index + 3]] = first + second
        # multiply
        elif op == '02':
            nincrement = 4
            if C == '0':
                # position
                first = program[program[index + 1]]
            else:
                # immediate
                first = program[index + 1]
            if B == '0':
                second = program[program[index + 2]]
            else:
                second = program[index + 2]
            assert A == '0'
            program[program[index + 3]] = first * second
        # input saved to address
        elif op == '03':
            nincrement = 2
            assert C == '0'
            addr = program[index + 1]
            program[addr] = input_value
        # output
        elif op == '04':
            nincrement = 2
            if C == '0':
                addr = program[index + 1]
            else:
                addr = index + 1
            prints.append(program[addr])
        # jump if true
        elif op == '05':
            if C == '0':
                first_param = program[program[index + 1]]
            else:
                first_param = program[index + 1]
            if B == '0':
                second_param = program[program[index + 2]]
            else:
                second_param = program[index + 2]
            if first_param != 0:
                jump = True
                new_index = second_param
            else:
                nincrement = 3
        # jump if false
        elif op == '06':
            if C == '0':
                first_param = program[program[index + 1]]
            else:
                first_param = program[index + 1]
            if B == '0':
                second_param = program[program[index + 2]]
            else:
                second_param = program[index + 2]
            if first_param == 0:
                jump = True
                new_index = second_param
            else:
                nincrement = 3
        # less than
        elif op == '07':
            nincrement = 4
            if C == '0':
                first = program[program[index + 1]]
            else:
                first = program[index + 1]
            if B == '0':
                second = program[program[index + 2]]
            else:
                second = program[index + 2]
            assert A == '0'
            if first < second:  # strict?
                program[program[index + 3]] = 1
            else:
                program[program[index + 3]] = 0
        # equals
        elif op == '08':
            nincrement = 4
            if C == '0':
                first = program[program[index + 1]]
            else:
                first = program[index + 1]
            if B == '0':
                second = program[program[index + 2]]
            else:
                second = program[index + 2]
            assert A == '0'
            if first == second:
                program[program[index + 3]] = 1
            else:
                program[program[index + 3]] = 0
        # end program
        elif op == '99':
            break
        else:
            raise NotImplementedError()
        if jump:
            index = new_index
            del new_index
        else:
            index = index + nincrement
            del nincrement
    return program, prints


assert run([1002, 4, 3, 4, 33], input_value=1)[0] == [1002, 4, 3, 4, 99]
assert run([1101, 100, -1, 4, 0], input_value=1)[0] == [1101, 100, -1, 4, 99]
program = list(map(int, open('data/input05').read().split(',')))
print(f'solution to part1: {run(program, input_value=1)[1][-1]}')
# we need to reload the program since we modify it in place...
program = list(map(int, open('data/input05').read().split(',')))
print(f'solution to part2: {run(program, input_value=5)[1][-1]}')
