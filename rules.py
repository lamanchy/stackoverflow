import functools
from math import *

# yvetsit values
# zvetsit text na programech
# type error, value error, stack overflow, zero division, timeout error
# co delat pri chybe
# napisu program aby delal stack overflow
from cards.function_card import FunctionCard
from cards.playing_card_back import PlayingCardBack
from cards.two_sided_card import TwoSidedCard


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
      lambda x: x * (x // 4),
      lambda x: sin(pi * x / 2) - 2,
      split_by_int,
      last_digit_negative,

      # 9
      if_greater_or_less,
      if_equal_or_not,
      for_cycle,
      while_cycle,

    ],
    "red": [  # 16 10KQJ
      # 10
      lambda x: ceil(sqrt(10 + x)),
      lambda x: floor(log2(90 - x)),
      int_from_list,
      ints_from_list,

      # # J can use floats
      lambda x: x + 0.5,
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
      rec_subtract,
      rec_divide,
      double_rec,
      rec_multiply,

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
  if x < 5:   return 66
  if x > 66:  return 5
  return 42


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def if_equal_or_not(x):
  if   x == 10:  x += 66
  elif x != 66:  x -= 10
  else:
    return x // 10

  return x


#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 7 !!!!!

def for_cycle(x):
  num = floor(x) % 5
  for _ in range(num):
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
  # index:  0123456789
  string = "176485923074"
  a = x % 10
  b = a + (x % 3) + 1
  return int(string[a:b])


def split_by_int(x):
  x = str(int(x) % 10)

  string = "376326492"
  parts = string.split(x)
  return len(parts) - 4


def last_digit_negative(x):
  digit = str(int(x))[-1]
  return -1 * int(digit)


#  MAX LINE LENGTH 29 SIGNS!!

def switch_places(x):
  y = abs(x)
  s = "{0:.2f}".format(y)
  a, b = s.split(".")
  result = float(b + "." + a)
  return result * sign(x)


#  MAX LINE LENGTH 29 SIGNS!!

def increment_digits(x):
  s = "{0:.2f}".format(x)
  for i in "9876543210":
    add = str(1 + int(i))[-1]
    s = s.replace(i, add)
  return float(s)


def reverse(x):
  string = str(abs(int(x)))
  string = string[::-1]
  res = int(string)
  return res * sign(x)


#  MAX LINE LENGTH 29 SIGNS!!

def subtract_madness(x):
  if isnan(x) or isinf(x):  # DEBUG this line wont be printed
    raise ValueError  # DEBUG this line wont be printed
  s = "{0:.2f}".format(x)
  s = s.replace('.', '--')
  return eval('-'.join(s))


@functools.lru_cache(None)
def rec_subtract(x):
  if x <= 0:
    return x

  x -= 60
  if x >= 0: x %= 60  # DEBUG this line wont be printed
  return rec_subtract(x)


@functools.lru_cache(None)
def rec_divide(x):
  if x == 0:
    return 0

  x = floor(x / 3)
  return sign(x) + \
         rec_divide(x)


#  MAX LINE LENGTH 29 SIGNS!!

@functools.lru_cache(None)
def double_rec(x):
  if -1 <= x <= 10: return -x

  res = double_rec(x // 100)
  res += double_rec(x // 10)
  return res


#  MAX LINE LENGTH 29 SIGNS!!


@functools.lru_cache(None)
def rec_multiply(x):
  if x % 8 == 0:
    return x

  res = rec_multiply(2 * x)
  return res - 1


def get_all_functions():
  fns = []
  for color in ["green", "yellow", "red"]:
    for fn in get_rules()[color]:
      fns.append(TwoSidedCard(FunctionCard(color, fn), PlayingCardBack("yellow")))

  return fns
