import inspect
import random
from math import *


def get_rules():
    return {
        "green": [  # 16 very simple  .... 2-5
            # 2
            # these four constants are missing in values
            lambda x: 7,
            lambda x: 13,
            lambda x: 16,
            lambda x: 19,
            # 3
            lambda x: x,
            lambda x: x + 5,
            lambda x: x + 11,
            lambda x: x - 1,
            # I would not substract more, so the result is never negative (0 in worst case)

            # 4
            lambda x: 2 * x,
            lambda x: min(x, 17),
            lambda x: x // 3,
            lambda x: max(x, 7),

            # 5
            lambda x: gcd(x, 24),
            lambda x: lcm(x, 6),
            lambda x: x if is_prime(x) else 1,
            lambda x: x % 5,
        ],
        "yellow": [  # 12 math, 8 very simple programs ... 6-10
            # 6
            lambda x: x - 25,
            lambda x: x - 128,
            lambda x: 151 - x,
            lambda x: 38 - x,

            # 7
            lambda x: x // -6,
            lambda x: -5 * x,
            lambda x: 100 // x,
            lambda x: x % 25,

            # 8
            lambda x: x * (x // 10),
            lambda x: ceil(sqrt(x)),
            lambda x: floor(log2(x)),
            lambda x: sin(pi * x / 2),

            # 9
            if_greater_or_less,
            if_equal_or_not,
            for_cycle,
            while_cycle,

            # 10
            int_from_list,
            ints_from_list,
            split_by_int,
            lambda x: int(str(x)[-1]),

        ],
        "red": [  # KQJ
            # J can use floats
            lambda x: x + 0.5,
            lambda x: -0.5 * x,
            lambda x: x / 1.5,
            lambda x: 1 / x,

            # Q float to string and back
            switch_places,
            put_and_eval,
            reverse,
            subtract_madness,

            # K
            rec_subtract,
            rec_divide,
            double_rec,
            rec_multiply,

        ],
        "white": [
            # A
            ackermann,
            lambda x: min(max(x, 10000), -10000),
            lambda x: pow(x, -x),
            lambda x: inf,
        ]
    }


def is_prime(n):
    if n != int(n):  return False
    if n <= 1:       return False

    for i in range(2, n):
        if (n % i) == 0:
            return False

    return True


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def if_greater_or_less(x):
    if x < 10:  return 66
    if x > 66:  return 10
    return 42


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def if_equal_or_not(x):
    if x == 10:
        x += 66
    elif x != 66:
        x -= 10
    else:
        return x // 10

    return x


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!

def for_cycle(x):
    for i in range(floor(x) % 5):
        x += 10

    return x


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!
def while_cycle(x):
    while x % 4 != 0:
        x = round(x / 5)

    return x


def int_from_list(x):
    string = "957812463"
    return int(string[x % 9])


def ints_from_list(x):
    string = "176485923074"
    first = x % 9
    second = first + (x % 3) + 1
    return int(string[first:second])


def split_by_int(x):
    string = "19754862315879625413"
    return len(string.split(str(x)))


def switch_places(x):
    string = "{0:.2f}".format(abs(x))
    a, b = string.split(".")
    a, b = b, a
    result = float(a + "." + b)
    copysign(x, result)
    return result


def put_and_eval(x):
    res = "{0:.2f}".format(x)
    res.replace('.', '-')
    return eval(res)


def reverse(x):
    x = abs(x)
    string = "{0:.2f}".format(x)
    return eval(string[::-1])


def subtract_madness(x):
    string = "{0:.2f}".format(x)
    string.replace('.', '--')
    return eval('-'.join(string))


def rec_subtract(x):
    if x <= 0:
        return x

    return rec_subtract(x - 30)


def rec_divide(x):
    if x == 0:
        return -1

    return -1 + rec_divide(round(x / 3))


def double_rec(x):
    x = abs(x)
    if x <= 1:
        return x

    return double_rec(x // 10) + \
           double_rec(x // 100)


def rec_multiply(x):
    if x % 8 != 0:
        return x

    return rec_multiply(2 * x) - 1


def ackermann(m, n=None):
    if n is None:  n = m
    if m == 0:     return n + 1

    if n == 0:
        return ackermann(m - 1, 1)

    return ackermann(
        m - 1,
        ackermann(m, n - 1)
    )


#  MAX LINE LENGTH 50 SIGNS!!!!!!!!!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 15 !!!!!!!!!!!!!!!!!!!!!!!!


def get_all_functions():
    fns = []
    for color in ["green", "yellow", "red", "white"]:
        for fn in get_rules()[color]:
            fns.append((fn, color))

    return fns


if __name__ == "__main__":
    from timeit import timeit

    for fn, color in get_all_functions():

        source_code = inspect.getsource(fn)

        # remove leading and ending spaces
        source_code = source_code.strip()

        if source_code.startswith("lambda") and source_code[-1] == ',':
            source_code = source_code[:-1]

        print(source_code)
        print(timeit("fn(3)", number=1000000, globals=globals()))

