from intcode import IntCodeComputer
import networkx as nx

inp1 = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..""".split('\n')


def prints2ascii(prints, prune=True):
    ascii_prints = "".join(map(chr, prints)).split('\n')
    if prune:
        ascii_prints = [row for row in ascii_prints if len(row) > 0]
    return ascii_prints


program = list(map(int, open('data/input17').read().split(',')))
computer = IntCodeComputer(program, resume=False)
prog_state, prints, status = computer.run([])
ascii_prints = prints2ascii(prints)


def is_intersection(r, c, ascii_prints):
    R, C = len(ascii_prints), len(ascii_prints[0])
    east, west, north, south = False, False, False, False
    if c > 0:
        if ascii_prints[r][c - 1] == '#':
            west = True
    if c < C - 1:
        if ascii_prints[r][c + 1] == '#':
            east = True
    if r > 0:
        if ascii_prints[r - 1][c] == '#':
            north = True
    if r < R - 1:
        if ascii_prints[r + 1][c] == '#':
            south = True
    return len(list(item for item in [east, west, north, south] if item)) > 2


assert is_intersection(0, 2, inp1) is False
assert is_intersection(2, 2, inp1) is True
assert is_intersection(3, 2, inp1) is False
assert is_intersection(4, 2, inp1) is True


def find_intersections(ascii_prints):
    intersections = []
    for r, row in enumerate(ascii_prints):
        for c, char in enumerate(row):
            if char == '#':
                if is_intersection(r, c, ascii_prints):
                    intersections.append((r, c))
    return intersections


assert len(find_intersections(inp1)) == 4

score = lambda items: items[0] * items[1]
assert sum(map(score, find_intersections(inp1))) == 76

intersections = find_intersections(ascii_prints)
print(f"solution for part1: {sum(map(score, intersections))}")

# part2
# find the right path by hand and compress it using IDE highlighting
path = 'R,4,R,12,R,10,L,12,L,12,R,4,R,12,' + \
       'L,12,R,4,R,12,L,12,L,8,R,10,L,12,L,8,R,10,' + \
       'R,4,R,12,R,10,L,12,L,12,R,4,R,12,' + \
       'L,12,R,4,R,12,L,12,L,8,R,10,R,4,R,12,R,10,L,12'

A = "R,4,R,12,R,10,L,12"
B = "L,12,R,4,R,12"
C = "L,12,L,8,R,10"

assert path.find(",".join([A, B, B, C, C, A, B, B, C, A])) == 0

# main
main = 'ABBCCABBCA'

# video feed option
feed = 'n'

message = []
message.extend([m for m in ",".join(main)] + ['\n'])
assert len(A) < 20
message.extend([inst for inst in A] + ['\n'])
message.extend([inst for inst in B] + ['\n'])
message.extend([inst for inst in C] + ['\n'])
message.extend([feed, '\n'])
message_ascii = [ord(val) for val in message]

# load the new program and run it
program[0] = 2
computer = IntCodeComputer(program, resume=False)
prog_state, prints, status = computer.run(input_values=message_ascii)
print(f"solution for part2: {prints[-1]}")
