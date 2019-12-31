# taken from https://github.com/mebeim/aoc/blob/master/2019/README.md#day-22---slam-shuffle

DEAL_NEW, DEAL_INC, CUT = 1, 2, 3

fin = open('data/input22').readlines()

moves = []
for l in fin:
    if 'deal into' in l:
        moves.append((DEAL_NEW, 0))
    elif 'deal with' in l:
        n = int(l[l.rfind(' '):])
        moves.append((DEAL_INC, n))
    elif 'cut' in l:
        n = int(l[l.rfind(' '):])
        moves.append((CUT, n))


def transform(start, step, size, moves):
    for move, n in moves:
        if move == DEAL_NEW:
            start = (start - step) % size
            step = -step % size
        elif move == DEAL_INC:
            step = (step * pow(n, size - 2, size)) % size
        elif move == CUT:
            if n < 0:
                n += size

            start = (start + step * n) % size

    return start, step


def repeat(start, step, size, repetitions):
    final_step = pow(step, repetitions, size)
    final_start = (start * (1 - final_step) * pow(1 - step, size - 2, size)) % size

    return final_start, final_step


start, step, size = 0, 1, 119315717514047
repetitions = 101741582076661

start, step = transform(start, step, size, moves)
start, step = repeat(start, step, size, repetitions)


value = (start + step * 2020) % size
print('solution for part2:', value)