import functools
from math import *


def get_rules():
  return {
    "green": [  # 16 very simple  .... 2-5
      # 2
      # these four constants are missing in values
      lambda x: 15,
      lambda x: 7,
      lambda x: 13,
      lambda x: 19,
      # 3
      lambda x: x,
      lambda x: x + 5,
      lambda x: x + 11,
      lambda x: x - 1,
      # I would not subtract more, so the result is never negative (0 in worst case)

      # 4
      lambda x: 2 * x,
      lambda x: min(x, 11),
      lambda x: ceil(x / 3),
      lambda x: max(x, 9),

      # 5
      lambda x: gcd(x, 24),
      lambda x: lcm(x, 6),
      if_prime,
      lambda x: (x % 5) + 1,
    ],
    "yellow": [  # 16 6-9
      # 6
      lambda x: x - 7,
      lambda x: x - 12,
      lambda x: 40 - x,
      lambda x: 10 - x,

      # 7
      lambda x: x // -4,
      lambda x: -2 * x + 40,
      lambda x: 50 // x,
      lambda x: x % 25,

      # 8
      lambda x: ceil(x / 4) ** 2,
      lambda x: sin(pi * x / 2) - 2,
      split_by_int,
      last_negative,

      # 9
      if_greater_or_less,
      if_equal_or_not,
      for_cycle,
      while_cycle,
    ],
    "red": [  # 16 10KQJ
      # 10
      lambda x: ceil(sqrt(10 + x)),
      lambda x: floor(log2(68 - x)),
      int_from_list,
      ints_from_list,

      # # J can use floats
      lambda x: x + 20.5,
      lambda x: -0.5 * x,
      lambda x: x / 1.5,
      lambda x: 1 / x,
      #
      # # Q float to string and back
      switch_places,
      increment_digits,
      reverse,
      # subtract_madness,  #####

      # K
      r_subtract,
      r_divide,
      double_r,
      r_multiply,

      # A
      lambda x: inf,
    ]
  }


def sign(x):
  if x == 0: return 0
  return copysign(1, x)


def is_prime(n):
  if n != int(n):  return False
  n = int(n)
  if n <= 1:       return False
  if n % 2 == 0 and n > 2:
    return False

  for i in range(3, int(sqrt(n)) + 1, 2):
    if n % i == 0:
      return False
  return True


def gcd(a, b):
  a = abs(a)
  b = abs(b)
  if a == 0: return b
  if b == 0: return a
  while b > 0:
    a, b = b, a % b
  return a


def lcm(a, b):
  if a == 0 or b == 0: return 0
  return abs(a * b) // gcd(a, b)


def if_prime(x):
  if x > 200: return 0
  if is_prime(x):
    return 17

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def if_greater_or_less(x):
  if x < 3:   return 33
  if x > 15:  return 28
  return 42


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def if_equal_or_not(x):
  if x == 10:
    x += 33
  elif x != 33:
    x -= 10
  else:
    return x // 10

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def for_cycle(x):
  count = floor(x) % 5
  for _ in range(count):
    x += 10

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!
def while_cycle(x):
  while x % 2 != 0:
    x = round(x / 3)

  return x


def int_from_list(x):
  # index:  0123456789
  string = "9578124630"
  return int(string[x % 10])


#  MAX LINE LENGTH 29 SIGNS!!
def ints_from_list(x):
  # index:  012345678
  string = "4269581730"
  a = x % 9
  b = a + (x % 2) + 1
  return int(string[a:b])


def split_by_int(x):
  x = str(int(x) % 10)

  string = "376326492"
  parts = string.split(x)
  return len(parts) - 4


def last_negative(x):
  digit = str(int(x))[-1]
  return -1 * int(digit)


#  MAX LINE LENGTH 29 SIGNS!!

def switch_places(x):
  # TODO coloring of that
  s = f"{abs(x):.2f}"
  a, b = s.split(".")
  result = float(b + "." + a)
  return result


#  MAX LINE LENGTH 29 SIGNS!!

def increment_digits(x):
  s = f"{x:.2f}"
  for i in "9876543210":
    new = str(1 + int(i))[-1]
    s = s.replace(i, new)
  return float(s)


def reverse(x):
  string = str(abs(int(x)))
  string = string[::-1]
  result = int(string)
  return result * sign(x)


#  MAX LINE LENGTH 29 SIGNS!!

def subtract_madness(x):
  if isnan(x) or isinf(x):  # DEBUG this line wont be printed
    raise ValueError  # DEBUG this line wont be printed
  s = f"{x:.2f}"
  s = s.replace('.', '--')
  return eval('-'.join(s))


@functools.lru_cache(None)
def r_subtract(x):
  if x <= 30:
    return x

  x -= 40
  if x >= 0: x %= 40  # DEBUG this line wont be printed
  return r_subtract(x)


@functools.lru_cache(None)
def r_divide(x):
  if x <= -1: raise RecursionError  # DEBUG this line wont be printed
  if x == 0:
    return 0

  x = floor(x / 3)
  return 10 + r_divide(x)


#  MAX LINE LENGTH 29 SIGNS!!

@functools.lru_cache(None)
def double_r(x):
  if -1 <= x <= 20: return x

  result = double_r(x // 100)
  result += double_r(x // 10)
  return result


#  MAX LINE LENGTH 29 SIGNS!!


@functools.lru_cache(None)
def r_multiply(x):
  if x % 4 == 0:
    return x

  result = r_multiply(2 * x)
  return result - 1
