from intcode import IntCodeComputer
from itertools import product


def _not(x, y):
    return not x


def _and(x, y):
    return x and y


def _or(x, y):
    return x or y


def run_simulation(springscript, abcdefghi_dict):
    local_vars = {'j': False, 't': False}
    local_vars.update(abcdefghi_dict)
    for op, var1, var2 in springscript:
        local_vars[var2] = op(local_vars[var1], local_vars[var2])
    return local_vars['j']


# configuration where drone should jump
should_jump = [(True, True, True, True, False, True, True, True, True),
               (False, True, True, True, True, True, True, True, True),
               (True, False, True, True, False, True, True, True, True),
               (True, True, True, True, False, False, True,True, False)]

# configurations where drone should not jump
should_not_jump = [(False, True, True, False, True, True, True, True, True),
                   (True, True, True, True, False, True, True, False, True),
                   [True, True, True, True, False, False, True, True, False]]

all_ops = list(product([_not, _and, _or], 'abcdefghijt', 'jt'))

found = False
for script_len in range(1, 16):
    print(f'starting script_len {script_len}')
    for script in product(all_ops, repeat=script_len):
        for abcdefghi, expected in zip(should_jump + should_not_jump,
                                       [True] * len(should_jump) + [False] * len(should_not_jump)):
            if run_simulation(script, dict(zip('abcdefghi', abcdefghi))) is not expected:
                break
        else:
            print('Found a solution script!')
            found = True
            break
    if found: break

input_map = {_and: 'AND', _or: 'OR', _not: 'NOT'}
out = ""
for op, var1, var2 in script:
    out += " ".join([input_map[op], var1.upper(), var2.upper()]) + '\n'
out += 'RUN\n'
print(out)
out_ascii = [ord(char) for char in out]
program = list(map(int, open('data/input21').read().strip().split(',')))
computer = IntCodeComputer(program, resume=False)
_, prints, status = computer.run(input_values=out_ascii)

message = "".join([chr(p) for p in prints if p < 128])
print(message)
