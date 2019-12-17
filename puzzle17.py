from intcode import IntCodeComputer
import numpy as np

program = list(map(int, open('data/input17').read().split(',')))
computer = IntCodeComputer(program, resume=False)
prog_state, prints, status = computer.run([])
ascii_prints = "".join(map(chr, prints)).split('\n')
ascii_prints = [row for row in ascii_prints if len(row) > 0]

inp1 = """..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..""".split('\n')


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

score = lambda items: items[0]* items[1]
assert sum(map(score, find_intersections(inp1))) == 76

intersections = find_intersections(ascii_prints)
print(f"solution for part1: {sum(map(score, intersections))}")

