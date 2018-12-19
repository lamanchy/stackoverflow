from math import *


def get_rules():
    return {
        "green": [  # 16 very simple  .... 2-5
            lambda x: 5,
            lambda x: 12,
            lambda x: 19,
            lambda x: x,
            lambda x: x + 5,
            lambda x: x + 11,
            #  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!

            # I would not substract more, so the result is never negative (0 in worst case)
            lambda x: x - 1,
            lambda x: min(x * 2, 20),
            lambda x: floor(x / 3),
            lambda x: max(x, 7),
            #     TODO 6 missing
        ],
        "yellow": [  # 12 math, 8 very simple programs ... 6-10
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
            #  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
            #     TODO 10 missing
        ],
        "red": [  # KQJ
            #     TODO 12 missing
            #     lambda x: sin(pi * x / 2),

        ],
        "white": [  # esa
            #     TODO 4 missing
            # black_goto_hell,
        ]
    }


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def yellow_if_1(x):
    if x < 10: return 66
    if x > 66: return 10
    return 42


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def yellow_if_2(x):
    if x != 10:
        x += 66
    elif x == 66:
        x -= 10
    else:
        return x / 10

    return x


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def yellow_for(x):
    for i in range(floor(x) % 5):
        x += 10

    return x


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!
def yellow_while(x):
    while x % 4 != 0:
        x = round(x / 3)

    asd = "string", 'string', "string'string'"

    # comment sdeeed

    return x


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!


def get_all_functions():
    fns = []
    for color in ["green", "yellow", "red", "white"]:
        for fn in get_rules()[color]:
            fns.append((fn, color))

    return fns
