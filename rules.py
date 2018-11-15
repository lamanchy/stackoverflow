from math import *


def get_rules():
    return [
        lambda x: x + 5,
        lambda x: abs(x - 3),
        lambda x: -2 * x,
        lambda x: 1,
        lambda x: floor(20 / x),
        lambda x: pow(x, 2) - 3 * x + 7,
        lambda x: pow(x - 1, x),
        lambda x: x % 7,
        lambda x: sin(pi * x / 2),
        fn_for,
    ]


def fn_for(x):
    result = 0
    for i in range(x-1, x+1):
        result += i

    return result
