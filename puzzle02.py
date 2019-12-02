def run(program):
    index = 0
    while True:
        op = program[index]
        # add
        if op == 1:
            first = program[program[index + 1]]
            second = program[program[index + 2]]
            program[program[index + 3]] = first + second
        elif op == 2:
            first = program[program[index + 1]]
            second = program[program[index + 2]]
            program[program[index + 3]] = first * second
        # end
        elif op == 99:
            break
        else:
            raise NotImplementedError()
        index = index + 4
    return program


def unit_tests():
    assert run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]
    return True


print(f"unit tests passed: {unit_tests()}")

# part 1
program = list(map(int, open('data/input02').read().split(',')))
program[1] = 12
program[2] = 2
print(f"solution to part1: {run(program)[0]}")

# part 2
for noun in range(100):
    for verb in range(100):
        program = list(map(int, open('data/input02').read().split(',')))
        program[1] = noun
        program[2] = verb
        output = run(program)[0]
        if output == 19690720:
            print(f"solution to part2: {100 * noun + verb}")
            break
