from intcode import IntCodeComputer
import itertools


def prints2ascii(prints, prune=True):
    ascii_prints = "".join(map(chr, prints)).split('\n')
    if prune:
        ascii_prints = [row for row in ascii_prints if len(row) > 0]
    return ascii_prints


program = list(map(int, open('data/input25').read().strip().split(',')))
computer = IntCodeComputer(program, resume=False)

cmds = """\
east
take manifold
south
take whirled peas
north
west
south
take space heater
south
take dark matter
north
east
north
west
south
take antenna
north
east
south
east
take bowl of rice
north
take klein bottle
north
take spool of cat6
west
"""

items = ['manifold', 'whirled peas', 'space heater', 'dark matter',
         'antenna', 'bowl of rice', 'klein bottle', 'spool of cat6']

tooheavy = 'A loud, robotic voice says "Alert! Droids on this ship are heavier than the detected value!" and you are ejected back to the checkpoint.'
toolight = 'A loud, robotic voice says "Alert! Droids on this ship are lighter than the detected value!" and you are ejected back to the checkpoint.'

# number of items to remove
for r in range(1, len(items)):
    for comb in itertools.combinations(items, r):
        new_cmds = cmds[:]
        for item in comb:
            new_cmds += f'drop {item}\n'
        new_cmds += 'north\n'
        ascii_cmds = [ord(char) for char in new_cmds]
        _, prints, status = computer.run(input_values=ascii_cmds)
        ascii_prints = prints2ascii(prints)
        if tooheavy in ascii_prints:
            continue
        elif toolight in ascii_prints:
            continue
        else:
            print(f'The following dropped items do not produce a "too light" or "too heavy" message: {comb}')
            break
