# basically copied from https://github.com/mebeim/aoc/tree/master/2019

from intcode import IntCodeComputer

springscript = """\
NOT A J
NOT J J
AND B J
AND C J
NOT J J
AND D J
WALK
"""

inp = list(map(ord, springscript))

program = list(map(int, open('data/input21').read().strip().split(',')))
computer = IntCodeComputer(program, resume=False)
_, prints, status = computer.run(input_values=inp)

message = "".join([chr(p) for p in prints if p < 128])
print(message)
print(f"solution for part1: {prints[-1]}")

# part2

springscript = """\
NOT C J
AND H J
NOT B T
OR T J
NOT A T
OR T J
AND D J
RUN
"""

inp = list(map(ord, springscript))
computer = IntCodeComputer(program, resume=False)
_, prints, status = computer.run(input_values=inp)
message = "".join([chr(p) for p in prints if p < 128])
print(message)
print(f"solution for part2: {prints[-1]}")
