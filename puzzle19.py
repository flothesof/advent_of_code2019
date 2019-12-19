from functools import lru_cache
import numpy as np
from intcode import IntCodeComputer, IntCodeStatus

program = list(map(int, open('data/input19').read().strip().split(',')))
computer = IntCodeComputer(program, resume=False)

coords = {}
for x in range(50):
    for y in range(50):
        _, prints, status = computer.run(input_values=[x, y])
        assert status == IntCodeStatus.TERMINATED
        coords[x + 1j * y] = prints[0]

beam = np.empty((50, 50))
for c, value in coords.items():
    r, c = int(c.imag), int(c.real)
    beam[r, c] = value

print(f"solution for part1: {int(beam.sum())}")

@lru_cache()
def get_beam_value(r, c):
    x, y = c, r
    _, beam_value, status = computer.run(input_values=[x, y])
    assert status == IntCodeStatus.TERMINATED
    assert len(beam_value) == 1
    return beam_value[0]


@lru_cache()
def get_left_boundary(r):
    c = 0
    while get_beam_value(r, c) != 1:
        c += 1
    return c


assert get_beam_value(10, get_left_boundary(10)) == 1
assert get_beam_value(10, get_left_boundary(10) - 1) == 0
assert get_beam_value(33, get_left_boundary(33)) == 1
assert get_beam_value(33, get_left_boundary(33) - 1) == 0

for i in range(4, 22):
    assert (beam[i, :] == 1).nonzero()[0].tolist()[0] == get_left_boundary(i)


@lru_cache()
def get_boundary_width(r):
    C = get_left_boundary(r)
    c = C
    while get_beam_value(r, c) == 1:
        c += 1
    return c - C


for i in range(4, 22):
    assert len((beam[i, :] == 1).nonzero()[0]) == get_boundary_width(i)

r = 10
found_square = False
left_boundary = get_left_boundary(r)
right_boundary = left_boundary
while get_beam_value(r, right_boundary) == 1:
    right_boundary += 1

while not found_square:
    if right_boundary + 1 - left_boundary >= 100:
        for c in range(left_boundary, right_boundary + 1):
            if get_beam_value(r, c + 99):
                if get_beam_value(r + 99, c):
                    if get_beam_value(r + 99, c + 99):
                        found_square = True
                        break
            else:
                break

    if not found_square:
        r += 1
        #  extend left and right boundary to next row
        while get_beam_value(r, left_boundary) == 0:
            left_boundary += 1
        assert get_beam_value(r, left_boundary) == 1
        while get_beam_value(r, right_boundary) == 1:
            right_boundary += 1
        right_boundary -= 1
        assert get_beam_value(r, right_boundary) == 1
        #print(f"I'm now at row {r}, left_boundary {left_boundary}, right_boundary {right_boundary}, width {right_boundary + 1 - left_boundary}")

# check solution
for rr in range(100):
    for cc in range(100):
        assert get_beam_value(r+rr, c + cc)

x = c
y = r
print(f"solution for part2: {10000 * x + y}")