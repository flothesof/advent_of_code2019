import re


def deal_into_new(stack):
    return list(reversed(stack))


assert deal_into_new(list(range(10))) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def cut(N, stack):
    if N > 0:
        left, right = stack[:N], stack[N:]
        return right + left
    elif N < 0:
        left, right = stack[:N], stack[N:]
        return right + left
    else:
        raise ValueError


assert cut(2, list(range(10))) == [2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
assert cut(3, list(range(10))) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
assert cut(-4, list(range(10))) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def increment(N, stack):
    indices = []
    L = len(stack)
    for index, val in enumerate(stack):
        index = N * index % L
        indices.append((index, val))
    indices.sort(key=lambda items: items[0])
    return [elem for ind, elem in indices]


assert increment(3, list(range(10))) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
assert increment(7, list(range(10))) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]


def apply_shuffle_process(ops, stack):
    new_stack = stack[:]
    for op in ops:
        new_stack = op(new_stack)
    return new_stack


test_ops1 = (lambda stack: increment(7, stack),
             deal_into_new,
             deal_into_new)
assert apply_shuffle_process(test_ops1, list(range(10))) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

test_ops2 = (lambda stack: cut(6, stack),
             lambda stack: increment(7, stack),
             deal_into_new)
assert apply_shuffle_process(test_ops2, list(range(10))) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

test_ops3 = (lambda stack: increment(7, stack),
             lambda stack: increment(9, stack),
             lambda stack: cut(-2, stack))
assert apply_shuffle_process(test_ops3, list(range(10))) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

test_ops4 = (deal_into_new,
             lambda stack: cut(-2, stack),
             lambda stack: increment(7, stack),
             lambda stack: cut(8, stack),
             lambda stack: cut(-4, stack),
             lambda stack: increment(7, stack),
             lambda stack: cut(3, stack),
             lambda stack: increment(9, stack),
             lambda stack: increment(3, stack),
             lambda stack: cut(-1, stack))
assert apply_shuffle_process(test_ops4, list(range(10))) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

stack = list(range(10007))

for line in open('data/input22').readlines():
    line = line.strip()
    m = re.match('cut (-?[\d]+)', line)
    if m is not None:
        N = int(m.groups()[0])
        stack = cut(N, stack)
        del N
        continue
    m = re.match('deal with increment ([\d]+)', line)
    if m is not None:
        M = int(m.groups()[0])
        stack = increment(M, stack)
        del M
        continue
    if line == 'deal into new stack':
        stack = deal_into_new(stack)
        continue
    print(f'could not parse {line}')

print(f"solution for part1: {stack.index(2019)}")
