import numpy as np


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
    """Returns first n values from the given iterator."""
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

input_signal = list(map(int, open('data/input16').read().strip()))
print(f"solution for part1: {''.join(map(str, apply_ntimes(input_signal, 100)[:8]))}")


# part2
def apply_second_ntimes_second_half_only(input_signal, n=1):
    N = len(input_signal)
    second = input_signal[N // 2:]
    output_signal = second[:]
    for _ in range(n):
        output_signal = abs(np.cumsum(output_signal[::-1])[::-1]) % 10
    return output_signal


assert apply_ntimes(list(map(int, "12345678")), 2)[-4:] == apply_second_ntimes_second_half_only(
    list(map(int, "12345678")), 2).tolist()
assert apply_ntimes(list(map(int, "12345678")), 20)[-4:] == apply_second_ntimes_second_half_only(
    list(map(int, "12345678")), 20).tolist()

long_input_signal = input_signal * 10000
offset = int("".join(map(str, long_input_signal[:7])))
start = offset - len(long_input_signal) // 2
second_half = apply_second_ntimes_second_half_only(long_input_signal, n=100)
print(f"solution for part2: {''.join(map(str, second_half[start: start + 8]))}")
