import numpy as np


def rcl_gen(r, c, layers):
    rr, cc, ll = 0, 0, 0
    while True:
        yield rr, cc, ll
        cc += 1
        if cc == c:
            cc = 0
            rr += 1
        if rr == r:
            rr = 0
            ll += 1
        if ll == layers:
            break


def make_img(r, c, layers, digits):
    gen = rcl_gen(r, c, layers)
    img = np.empty((r, c, layers), int)
    for ind, value in zip(gen, digits):
        img[ind] = value
    return img


# unit test part1
digits = list(map(int, '123456789012'))
r, c = 2, 3
layers = len(digits) // (r * c)
img = make_img(r, c, layers, digits)
assert np.allclose(img[:, :, 0], np.array([[1, 2, 3],
                                           [4, 5, 6]]))

# part 1
digits = list(map(int, open('data/input08').read().strip()))
r, c = 6, 25
layers = len(digits) // (r * c)
img = make_img(r, c, layers, digits)
layer_argmin = np.argmin((img == 0).sum(axis=0).sum(axis=0))
print(f'solution for part1: {(img[:, :, layer_argmin] == 1).sum() * (img[:, :, layer_argmin] == 2).sum()}')


def to_img(vals):
    for val in vals:
        # 2 = transparent
        if val != 2:
            return val


def make_msg(img):
    msg = np.empty(img.shape[:2], int)
    for rr in range(r):
        for cc in range(c):
            vals = img[rr, cc, :]
            msg[rr, cc] = to_img(vals)
    return msg


# unit test part2
digits = list(map(int, '0222112222120000'))
r, c = 2, 2
layers = len(digits) // (r * c)
img = make_img(r, c, layers, digits)
msg = make_msg(img)
assert np.allclose(msg, np.array([[0, 1],
                                  [1, 0]]))

# part2
digits = list(map(int, open('data/input08').read().strip()))
r, c = 6, 25
layers = len(digits) // (r * c)
img = make_img(r, c, layers, digits)
msg = make_msg(img)

import matplotlib.pyplot as plt

plt.imshow(msg)
plt.show()
