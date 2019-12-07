from itertools import permutations


def run(input_program, input_values):
    program = input_program[:]
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
            if len(input_values) > 0:
                input_value = input_values.pop(0)
                program[addr] = input_value
            else:
                # we need to wait, so we just exit
                return program, prints, False
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
    return program, prints, True


def iterate(program, seq):
    state, prints, is_finished = run(program, input_values=[seq[0], 0])
    state, prints, is_finished = run(program, input_values=[seq[1], prints[0]])
    state, prints, is_finished = run(program, input_values=[seq[2], prints[0]])
    state, prints, is_finished = run(program, input_values=[seq[3], prints[0]])
    state, prints, is_finished = run(program, input_values=[seq[4], prints[0]])
    return prints[0]


# unit tests part1
program = list(map(int, "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0".split(',')))
assert iterate(program, [4, 3, 2, 1, 0]) == 43210
program = list(map(int, "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0".split(',')))
assert iterate(program, [0, 1, 2, 3, 4]) == 54321
program = list(map(int,
                   "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0".split(
                       ',')))
assert iterate(program, [1, 0, 4, 3, 2]) == 65210

# part1 solution
program = list(map(int, open('data/input07').read().split(',')))
all_perms = permutations([0, 1, 2, 3, 4])
print(f'solution for part1: {max(iterate(program, seq) for seq in all_perms)}')


# part2 new code
def iterate_feedback(program, seq):
    inp1 = [seq[0], 0]
    is_finished = False
    while not is_finished:
        state, prints, is_finished = run(program, input_values=inp1)
        inp2 = [seq[1], *prints]
        state, prints, is_finished = run(program, input_values=inp2)
        inp3 = [seq[2], *prints]
        state, prints, is_finished = run(program, input_values=inp3)
        inp4 = [seq[3], *prints]
        state, prints, is_finished = run(program, input_values=inp4)
        inp5 = [seq[4], *prints]
        state, prints, is_finished = run(program, input_values=inp5)
        inp1 = [seq[0], 0, *prints]
    return prints[-1]


# unit tests part2
program = list(
    map(int, "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5".split(',')))
assert iterate_feedback(program, [9, 8, 7, 6, 5]) == 139629729
program = list(map(int,
                   "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10".split(
                       ',')))
assert iterate_feedback(program, [9, 7, 8, 5, 6]) == 18216

# part2 solution
program = list(map(int, open('data/input07').read().split(',')))
all_perms = permutations([5, 6, 7, 8, 9])
print(f'solution for part2: {max(iterate_feedback(program, seq) for seq in all_perms)}')
