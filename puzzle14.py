from math import ceil
from math import log10

inp1 = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

inp2 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

inp3 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

inp4 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

inp5 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""


def to_tuple(str):
    """'1 FUEL'-> (1, FUEL)"""
    prod_qty, prod_name = str.split(' ')
    return (int(prod_qty), prod_name)


def parse_input_with_weights(inp):
    weighted_reactions = {}
    for line in inp.split('\n'):
        reactants, prod = line.split(' => ')
        weighted_reactions[to_tuple(prod)] = list(map(to_tuple, reactants.split(', ')))
    return weighted_reactions


def get_key(product, weighted_reactions):
    return next(key for key in weighted_reactions.keys() if key[1] == product)


def get_reactants(product, weighted_reactions):
    key = get_key(product, weighted_reactions)
    return weighted_reactions[key]


def compute_quantities(product, qty, reactants, reaction_products):
    reaction_product_weight, _ = reaction_products
    replaced = []
    # easy case
    if reaction_product_weight == 1:
        for r_qty, r_name in reactants:
            replaced.append([r_name, r_qty * qty])
    else:
        # we get it exactly right
        n_reactions = int(ceil(qty / reaction_product_weight))
        for r_qty, r_name in reactants:
            replaced.append([r_name, r_qty * n_reactions])
        if not qty % reaction_product_weight == 0:
            # surplus
            replaced.append([product, qty - n_reactions * reaction_product_weight])
    return replaced


def sum_production_needs(production_needs):
    products = set(prod for prod, qty in production_needs)
    return [(prod, sum([q for p, q in production_needs if p == prod])) for prod in products]


def solve(inp, debug=False, start_fuel=1):
    weighted_reactions = parse_input_with_weights(inp)
    production_needs = [('FUEL', start_fuel)]
    while True:
        # have we reduced everything to ORE?
        if all(prod_name == 'ORE' for (prod_name, prod_qty) in production_needs if prod_qty >= 0):
            break
        # simplify
        else:
            if debug: print(f"production needs: {production_needs}")
            if len(production_needs) > 0:
                product, qty = next(items for items in production_needs if items[0] != 'ORE' if items[1] >= 0)
                reaction_products = get_key(product, weighted_reactions)
                reactants = get_reactants(product, weighted_reactions)
                replaced = compute_quantities(product, qty, reactants, reaction_products)
                production_needs.remove((product, qty))
                production_needs = replaced + production_needs
                production_needs = sum_production_needs(production_needs)
    if debug: print(f"production needs: {production_needs}")
    return production_needs


get_ore = lambda production_needs: next(qty for prod, qty in production_needs if prod == 'ORE')
assert get_ore(solve(inp1)) == 31
assert get_ore(solve(inp2)) == 165
assert get_ore(solve(inp3)) == 13312
assert get_ore(solve(inp4)) == 180697
assert get_ore(solve(inp5)) == 2210736
print('all tests passed for part1')
print(f"solution for part1: {get_ore(solve(open('data/input14').read().strip()))}")


def search_max_fuel(inp, max_ore=1000000000000):
    ore_per_fuel = get_ore(solve(inp))
    fuel = 10 ** (int(log10(max_ore / ore_per_fuel)))
    step = 10 * fuel
    assert get_ore(solve(inp, start_fuel=fuel)) < max_ore
    assert get_ore(solve(inp, start_fuel=fuel + step)) > max_ore
    while True:
        next_val = get_ore(solve(inp, start_fuel=fuel + step))
        if next_val > max_ore:
            step = int(step / 10)
            if step < 1:
                break
        else:
            fuel = fuel + step
    return fuel


assert search_max_fuel(inp3) == 82892753
assert search_max_fuel(inp4) == 5586022
assert search_max_fuel(inp5) == 460664
print('all tests passed for part2')
print(f"solution for part1: {search_max_fuel(open('data/input14').read().strip())}")
