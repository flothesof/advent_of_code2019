def fuel_requirement(module):
    return int(module / 3) - 2


def unit_tests():
    assert fuel_requirement(12) == 2
    assert fuel_requirement(14) == 2
    assert fuel_requirement(1969) == 654
    assert fuel_requirement(100756) == 33583
    assert fuel_requirement_recursive(14) == 2
    assert fuel_requirement_recursive(1969) == 966
    assert fuel_requirement_recursive(100756) == 50346
    return True


def fuel_requirement_recursive(module):
    fuel = fuel_requirement(module)
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_requirement_recursive(fuel)


print(f"unit tests passed: {unit_tests()}")

modules = [int(line) for line in open('data/input01').readlines()]
print(f"solution for part1: {sum(fuel_requirement(module) for module in modules)}")
print(f"solution for part2: {sum(fuel_requirement_recursive(module) for module in modules)}")
