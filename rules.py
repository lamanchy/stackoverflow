import inspect
import random
from math import *


# yvetsit values
# zvetsit text na programech
# type error, value error, stack overflow, zero division, timeout error
# co delat pri chybe
# napisu program aby delal stack overflow

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
      if_prime,
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
      lambda x: ceil(sqrt(abs(x))),
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
      rec_sub,
      rec_divide,
      d_rec,
      rec_mul,

    ],
    "black": [
      # A
      ack,
      lambda x: min(x, -10000),
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


def if_prime(x):
  if is_prime(x):
    return x

  return 1


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def if_greater_or_less(x):
  if x < 10:  return 66
  if x > 66:  return 10
  return 42


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def if_equal_or_not(x):
  if x == 10:   x += 66
  elif x != 66: x -= 10
  else:  return x // 10

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def for_cycle(x):
  num = floor(x) % 5
  for i in range(num):
    x += 10

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!
def while_cycle(x):
  while x % 4 != 0:
    x = round(x / 5)

  return x


def int_from_list(x):
  # index:  012345678
  string = "957812463"
  return int(string[x % 9])


#  MAX LINE LENGTH 29 SIGNS!!
def ints_from_list(x):
  # index:  0123456789
  string = "176485923074"
  a = x % 9
  b = a + (a % 3) + 1
  return int(string[a:b])


def split_by_int(x):
  x = str(int(x) % 10)
  string = "1975486231587962"
  parts = string.split(x)
  return len(parts)


#  MAX LINE LENGTH 29 SIGNS!!

def switch_places(x):
  y = abs(x)
  s = "{0:.2f}".format(y)
  a, b = s.split(".")
  result = float(b + "." + a)
  copysign(-1*x, result)
  return result


#  MAX LINE LENGTH 29 SIGNS!!

def put_and_eval(x):
  res = "{0:.2f}".format(x)
  res.replace('.', '-')
  return eval(res)


def reverse(x):
  string = str(abs(int(x)))
  reversed = string[::-1]
  copysign(x, string)
  return string


#  MAX LINE LENGTH 29 SIGNS!!

def subtract_madness(x):
  s = "{0:.2f}".format(x)
  s = s.replace('.', '--')
  return eval('-'.join(s))


def rec_sub(x):
  if x <= 0:
    return x

  return rec_sub(x - 30)


def rec_divide(x):
  if x == 0:
    return -1

  x = round(x / 3)
  return -1 + rec_divide(x)


#  MAX LINE LENGTH 29 SIGNS!!

def d_rec(x):
  x = abs(x)
  if x <= 1: return x

  return d_rec(x // 10) + \
         d_rec(x // 100)


#  MAX LINE LENGTH 29 SIGNS!!

def rec_mul(x):
  if x % 8 != 0:
    return x

  return rec_mul(2 * x) - 1


#  MAX LINE LENGTH 29 SIGNS!!
def ack(m, n=None):
  if n is None:  n = m
  if m == 0:     return n + 1
  if n == 0:     n = 1
  else:
    n = ack(m, n - 1)
  return ack(m - 1, n)


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!


def get_all_functions():
  fns = []
  for color in ["green", "yellow", "red", "black"]:
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
