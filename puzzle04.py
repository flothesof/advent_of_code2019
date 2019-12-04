def rules_apply(digits):
    str_digits = str(digits)
    adj_digits = [str_digits[:2],
                  str_digits[1:3],
                  str_digits[2:4],
                  str_digits[3:5],
                  str_digits[4:6]]
    if not min(len(set(adj)) for adj in adj_digits) == 1:
        return False
    if not "".join(sorted(str_digits)) == str_digits:
        return False
    return True


def rules_apply_part2(digits):
    str_digits = str(digits)
    if not "".join(sorted(str_digits)) == str_digits:
        return False
    adj_digits = [str_digits[:2],
                  str_digits[1:3],
                  str_digits[2:4],
                  str_digits[3:5],
                  str_digits[4:6]]
    adjacent_pair = [len(set(adj)) == 1 for adj in adj_digits]
    if not any(adjacent_pair):
        return False
    at_least_one = False
    for index, is_pair in enumerate(adjacent_pair):
        if not is_pair:
            continue
        if index == 0:
            if not adjacent_pair[1]:
                at_least_one = True
        elif index == 4:
            if not adjacent_pair[3]:
                at_least_one = True
        else:
            same_left = adjacent_pair[index - 1]
            same_right = adjacent_pair[index + 1]
            if not same_left and not same_right:
                at_least_one = True
    if not at_least_one:
        return False
    return True


# tests
assert rules_apply_part2(112233)
assert not rules_apply_part2(123444)
assert rules_apply_part2(111122)

password_range = (272091, 815432)
valid = []
valid_part2 = []
for digits in range(password_range[0], password_range[1] + 1):
    if rules_apply(digits):
        valid.append(digits)
    if rules_apply_part2(digits):
        valid_part2.append(digits)

print(f"solution to part1: {len(valid)}")
print(f"solution to part2: {len(valid_part2)}")
