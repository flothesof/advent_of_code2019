def gen_pattern(output_elem):
    pattern = []
    base_pattern = [0, 1, 0, -1]
    for elem in base_pattern:
        pattern.extend([elem for _ in range(output_elem)])
    return pattern


assert gen_pattern(1) == [0, 1, 0, -1]
assert gen_pattern(2) == [0, 0, 1, 1, 0, 0, -1, -1]


def pattern_iter(pattern, index=0, skipped_first=False):
    while True:
        if index == 0:
            if not skipped_first:
                skipped_first = True
            else:
                yield pattern[index]
        else:
            yield pattern[index]
        index = (index + 1) % len(pattern)


def take(n, iter):
    """Returns first n values from the given sequence."""
    result = []
    try:
        for i in range(n):
            result.append(next(iter))
    except StopIteration:
        pass
    return result


assert take(15, pattern_iter(gen_pattern(2))) == [0, 1, 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1]


def keep_ones_digit(n):
    return int(str(n)[-1])


def apply(input_signal, debug=False):
    output_signal = []
    for output_phase in range(1, len(input_signal) + 1):
        if debug: debug_str = ""
        iter = pattern_iter(gen_pattern(output_phase))
        s = 0
        for i, p in zip(input_signal, iter):
            s += i * p
            if debug: debug_str += f"{i: 2}*{p: 2} + "
        s = keep_ones_digit(s)
        if debug: debug_str = debug_str[:-3] + f" = {s}"; print(debug_str)
        output_signal.append(s)
    return output_signal


assert apply(list(map(int, "12345678"))) == list(map(int, "48226158"))
assert apply(list(map(int, "48226158"))) == list(map(int, "34040438"))
assert apply(list(map(int, "34040438"))) == list(map(int, "03415518"))
assert apply(list(map(int, "03415518"))) == list(map(int, "01029498"))


def apply_ntimes(input_signal, n):
    signal = input_signal[:]
    for _ in range(n):
        signal = apply(signal)
    return signal


assert apply_ntimes(list(map(int, "12345678")), 4) == list(map(int, "01029498"))
assert apply_ntimes(list(map(int, "80871224585914546619083218645595")), 100)[:8] == list(map(int, "24176176"))
assert apply_ntimes(list(map(int, "19617804207202209144916044189917")), 100)[:8] == list(map(int, "73745418"))
assert apply_ntimes(list(map(int, "69317163492948606335995924319873")), 100)[:8] == list(map(int, "52432133"))


# print(f"solution for part1: {''.join(map(str, apply_ntimes(list(map(int, open('data/input16').read().strip())), 100)[:8]))}")


def apply2(input_signal, debug=False):
    output_signal = []
    for output_phase in range(1, len(input_signal) + 1):
        if debug: debug_str = ""
        iter = pattern_iter(gen_pattern(output_phase), index=output_phase, skipped_first=True)
        s = 0
        for i, p in zip(input_signal[output_phase - 1:], iter):
            s += i * p
            if debug: debug_str += f"{i: 2}*{p: 2} + "
        s = keep_ones_digit(s)
        if debug: debug_str = debug_str[:-3] + f" = {s}"; print(debug_str)
        output_signal.append(s)
    return output_signal


take(15, pattern_iter(gen_pattern(2)))
take(15, pattern_iter(gen_pattern(2), index=1, skipped_first=True))

apply(list(map(int, "12345678")), debug=True)
apply2(list(map(int, "12345678")), debug=True)
assert apply2(list(map(int, "12345678"))) == list(map(int, "48226158"))


def apply_ntimes2(input_signal, n):
    signal = input_signal[:]
    for _ in range(n):
        signal = apply2(signal)
    return signal


assert apply_ntimes2(list(map(int, "12345678")), 4) == list(map(int, "01029498"))
assert apply_ntimes2(list(map(int, "80871224585914546619083218645595")), 100)[:8] == list(map(int, "24176176"))
assert apply_ntimes2(list(map(int, "19617804207202209144916044189917")), 100)[:8] == list(map(int, "73745418"))
assert apply_ntimes2(list(map(int, "69317163492948606335995924319873")), 100)[:8] == list(map(int, "52432133"))

# part2 investigate symetry:
apply(list(map(int, "12345678")), debug=True)
apply2(list(map(int, "12345678")), debug=True)
import numpy as np
import matplotlib.pyplot as plt

input_len = 10
coef_mat = np.empty((input_len, input_len))
for output_phase in range(1, input_len + 1):
    iter = pattern_iter(gen_pattern(output_phase))
    row = take(input_len, iter)
    print(row)
    coef_mat[output_phase - 1] = row

plt.imshow(coef_mat)

#print(f"solution for part1: {''.join(map(str, apply_ntimes2(list(map(int, open('data/input16').read().strip())), 100)[:8]))}")