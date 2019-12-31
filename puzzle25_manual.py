def prints2ascii(prints, prune=True):
    ascii_prints = "".join(map(chr, prints)).split('\n')
    if prune:
        ascii_prints = [row for row in ascii_prints if len(row) > 0]
    return ascii_prints


from intcode import IntCodeComputer

program = list(map(int, open('data/input25').read().strip().split(',')))
computer = IntCodeComputer(program, resume=True)

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

ascii_cmds = [ord(char) for char in cmds]
_, prints, status = computer.run(input_values=ascii_cmds)

while True:
    cmd = input()
    ascii_cmd = [ord(char) for char in cmd + '\n']
    _, prints, status = computer.run(input_values=ascii_cmd)
    for line in prints2ascii(prints):
        print(line)
    computer.state = computer.state[:-1] + ([],)
