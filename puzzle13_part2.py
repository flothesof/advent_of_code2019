from puzzle09 import load_addr, load_param, write, is_valid


def get_player_ball_ntiles(prints):
    player, ball = None, None
    screen = dict()
    for x, y, tile_id in zip(prints[::3], prints[1::3], prints[2::3]):
        if x >= 0:
            if tile_id == 3:
                player = x, y
            elif tile_id == 4:
                ball = x, y
            pixel = x - 1j * y
            screen[pixel] = tile_id
    ntiles = sum([1 for val in screen.values() if val == 2])
    return player, ball, ntiles


def run_with_gameai(input_program, input_values):
    program = input_program[:]
    index = 0
    relative_base = 0
    extra_mem = {}
    prints = []
    while True:
        instruction = program[index]
        op_str = f"{instruction:05}"  # pad with zeros if necessary
        op = op_str[-2:]
        mode_param3, mode_param2, mode_param1 = op_str[0], op_str[1], op_str[2]
        jump = False
        # add
        if op == '01':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            write(program, write_addr, param1 + param2, extra_mem)
            index += nincrement
        # multiply
        elif op == '02':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            write(program, write_addr, param1 * param2, extra_mem)
            index += nincrement
        # input_value written to address
        elif op == '03':
            nincrement = 2
            write_addr = load_addr(program, index + 1, mode_param1, relative_base)
            if len(input_values) > 0:
                input_value = input_values.pop(0)
            else:
                # determine move automatically with "AI"
                player, ball, ntiles = get_player_ball_ntiles(prints)
                assert player is not None
                assert ball is not None
                if ball[0] > player[0]:
                    move = 1  # right
                elif ball[0] < player[0]:
                    move = -1  # left
                else:
                    move = 0  # neutral
                input_value = move
                if ntiles == 0:
                    return program, prints, False
            write(program, write_addr, input_value, extra_mem)
            index += nincrement
        # output parameter
        elif op == '04':
            nincrement = 2
            addr = load_addr(program, index + 1, mode_param1, relative_base)
            if is_valid(addr, program):
                prints.append(program[addr])
            elif addr in extra_mem:
                prints.append(extra_mem[addr])
            else:
                raise ValueError
            index += nincrement
        # jump if true
        elif op == '05':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            if param1 != 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # jump if false
        elif op == '06':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            if param1 == 0:
                index = param2
            else:
                nincrement = 3
                index += nincrement
        # less than
        elif op == '07':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            if param1 < param2:  # strict?
                write(program, write_addr, 1, extra_mem)
            else:
                write(program, write_addr, 0, extra_mem)
            index += nincrement
        # equals
        elif op == '08':
            nincrement = 4
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            param2 = load_param(program, index + 2, mode_param2, extra_mem, relative_base)
            write_addr = load_addr(program, index + 3, mode_param3, relative_base)
            if param1 == param2:
                write(program, write_addr, 1, extra_mem)
            else:
                write(program, write_addr, 0, extra_mem)
            index += nincrement
        # adjust relative base
        elif op == '09':
            param1 = load_param(program, index + 1, mode_param1, extra_mem, relative_base)
            relative_base += param1
            index += 2
        # end program
        elif op == '99':
            return program, prints, True
        else:
            raise NotImplementedError()


def prints2score(prints, debug=False):
    scores = []
    for x, y, tile_id in zip(prints[::3], prints[1::3], prints[2::3]):
        if x == -1:
            if debug: print(f"score: {tile_id}")
            scores.append(tile_id)
    return scores


# part2
program = list(map(int, open('data/input13').read().split(',')))
program[0] = 2
state, prints, is_finished = run_with_gameai(program, input_values=[])
scores = prints2score(prints)
print(f"solution for part2: {scores[-1]}")
