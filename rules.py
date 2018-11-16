from math import *


def get_rules():
    return {
        "green": [  # 10 very simple
            lambda x: 5,
            lambda x: 12,
            lambda x: 19,
            lambda x: x,
            lambda x: x + 5,
            lambda x: x + 11,
            lambda x: x - 1,  # I would not substract more, so the result is never negative (0 in worst case)
            lambda x: min(x * 2, 20),
            lambda x: floor(x / 3),
            lambda x: max(x, 7),
        ],
        "yellow": [  # 6 math, 4 very simple programs
            lambda x: x - 13,
            lambda x: 151 - x,
            lambda x: x / -6,
            lambda x: abs(3 * x),
            lambda x: floor(50 / x),
            lambda x: x % 20,
            yellow_if_1,
            yellow_if_2,
            yellow_for,
            yellow_while,
        ],
        "red": [
            #     lambda x: sin(pi * x / 2),

        ],
        "black": [
            # black_goto_hell,
        ]
    }


def yellow_if_1(x):
    if x < 10: return 66
    if x > 66: return 10
    return 42


def yellow_if_2(x):
    if x != 10:
        x += 66
    elif x == 66:
        x -= 10
    else:
        return x / 10

    return x


def yellow_for(x):
    for i in range(floor(x) % 5):
        x += 10

    return x


def yellow_while(x):
    while x % 4 != 0:
        x = round(x / 3)

    return x
