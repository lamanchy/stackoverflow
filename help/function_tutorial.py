from cards.text_help_card import TextHelpCard

# 27 lines max
from cards.title_help_card import TitleHelpCard

function_tutorial = [
  TitleHelpCard("How to use\nfunctions", "(gets handy)", "green"),
  TextHelpCard("green", "## How to use a function", """\
# There are two ways to write a function:
lambda x: x + 5
# "lambda x" marks a function without 
# a name with one input argument x

# "x + 5" is a result, inputted number
# raised by 5, so for 11 it returns 16

# or:
def add_and_multiply(x):
  x += 1
  return x * 2

# "add_and_multiply" is a named function,
# it again has one input argument x

# this function firstly raises input by 1,
# then returns double of that, so
# for example for input 3 it returns 8

# you can chain more functions together,
# so if we chain first and second function
# on number 1, that gives us 1 -> 6 -> 14,
# but we can change the order
# of the functions, which gives us
# 1 -> 4 -> 9, a different result\
"""),
  TextHelpCard("green", "## Help for ① cards", """\
lambda x: 15
# a constant function, it returns number
# 15 for any input value
① 1 -> 15, -2 -> 15
# 1 -> 15 is an example that this function
# for input value 1 returns value 15

lambda x: x
# the inputted value is returned as is
① 1 -> 1, 2 -> 2, 12 -> 12

lambda x: x + 5
① 1 -> 6, 7 -> 12

lambda x: 2 * x
# "*" marks multiplication
① 1 -> 2, 3 -> 6

lambda x: max(x, 9)
# maximum of two numbers returns always
# the greater one
① 7 -> 9, 9 -> 9, 14 -> 14

lambda x: min(x, 11)
# "min" works equivalently to max
① 1 -> 1, 11 -> 11, 16 -> 11\
"""),
  TextHelpCard("green", "", """\
lambda x: ceil(x / 3)
# "/" is a symbol for a division, x is 
# divided as a real number, "ceil" rounds
# number always up. E.g. 4 / 3 is one plus
# a bit, rounded up returns two
① 1 -> 1, 2 -> 1, 3 -> 1, 4 -> 2

lambda x: gcd(x, 12)
# greatest common divisor of x and 12,
# it is the greatest of all numbers,
# which divide both x and 12
① 10 -> 2, 6 -> 6, 16 -> 4

lambda x: lcm(x, 4)
# lowest common multiple is a lowest
# of all numbers divisible by both 4 and x
① 2 -> 4, 3 -> 12, 6 -> 12

lambda x: (x % 5) + 1
# "%" marks a reminder, e.g. 22 divided
# by 5 is 4, with reminder of 2, this 
# function would return 3 (2 + 1)
① 1 -> 2, 7 -> 3, 10 -> 1

def if_prime # definition is on a card
# number is a prime, when it is divisible
# by only two numbers, 1 and itself
① 1 -> 1, 2 -> 17, 4 -> 4, 5 -> 17\
"""),
  TextHelpCard("green", "## If, elif and else statements", """\
def if_func(x):
  if x > 5:   x += 1
  if x > 3:   x += 2
  elif x < 1: x += 3
  else:       x += 4
  return x + 10

# second line (x += 1) is executed only
# if x is greater than 5

# third line (x += 2) is executed only
# if x is greater than 3

# elif is a shortcut for "else if",
# therefore x is raised by two only if x
# is less than 1 AND is not bigger than 3

# x += 3 is executed when both conditions
# above are False, only if x is 1, 2 or 3

# the part without indent (return x + 10)
# is not affected by if statements and
# is executed always

if x > 5:  # two line equivalent
  x += 1   # of the first if statement\
"""),
  TextHelpCard("yellow", "## Help for ② cards", """\
# just a reminder, some combinations
# of cards might get ugly results, so
# if you cannot calculate something
# in your head, then don't use it, or
# just use an approximation (being closer 
# to result than your opponent is enough)

# signs ①②③ shows, that the example is
# relevant for specific difficulty only,
# you can ignore examples for higher
# difficulties than you play

lambda x: ceil(x / 3)
# ceil rounds up, ceil of -0.5 is 0 not -1
② -3 -> -1, -2 -> 0, 0 -> 0

lambda x: x // -6
# x // y is equivalent to floor(x / y),
# floor rounds always down
# 1 // -2 is floor(-0.5) which is -1 
② 0 -> 0, 1 -> -1, 6 -> -1, 7 -> -2
③ 6.1 -> -2

def if_prime
# only natural number can be a prime
② 0 -> 0, -5 -> -5
③ 3.5 -> 3.5, 200 -> 200, 201 -> 0\
"""),
  TextHelpCard("yellow", "", """\
lambda x: 100 // x
# "how many times x fits into 100"
② 3 -> 33, -5 -> -20
③ -3.3 -> -30

lambda x: gcd(x, 12)  # green cards
② 0 -> 12, -5 -> 1    # might get tricky
③ 1.5 -> 1.5, -3.5 -> 0.5, inf -> 12

lambda x: lcm(x, 4)
② 0 -> 0, -5 -> 20
③ 1.5 -> 12, 2.5 -> 20, inf -> inf

lambda x: sin(pi * x / 2) - 2
# sin(0) is 0, sin(pi/2) is 1
# sin(pi) is 0, sin(3*pi/2) is -1
② 0 -> -2, 4 -> -2, 5 -> -1, -1 -> -3
③ 2.2 -> -2 > res > -3, inf -> ValueError

lambda x: (x % 5) + 1
② -2 -> 4, -9 -> 2
③ 5.5 -> 1.5, -9.5 -> 1.5, inf -> 1

def if_greater_or_less
# see if statements two pages back
② 0 -> 66, 5 -> 42, 42 -> 42, 99 -> 5

def if_equal_or_not
② 10 -> 76, 20 -> 10, 66 -> 6\
"""),
  TextHelpCard("yellow", "## For and while statements", """\
for _ in range(num):
  x -= 1  # these two statements are
  x *= 2  # executed num-times

def for_cycle
② 0 -> 0, 1 -> 11, 9 -> 44, 10 -> 10

while x > 0: x -= 1
# x -= 1 is executed over and over,
# as long as x is bigger than zero

def while_cycle
# "round" rounds number to closest whole
# number, 0.5 is rounded always up
② 2 -> 2, 5 -> 2, 3 -> 0, 11 -> 4
③ 2.2 -> 0, -4.9 -> -2

def split_by_int
# int(x) equals to x // 1, int(0.8) is 0
# "1213".split("1") == ["", "2", "3"]
# len(list) == number of items in list
② 0 -> -3, 2 -> -1, 7 -> -2

def last_digit_negative
# [-1] takes last item from a list
② 2 -> -2, 31 -> -1, -23 -> -3\
"""),
  TextHelpCard("red", "## Help for ③ cards", """\
# well, functions might get bit tricky
# down the road, so if you are in need of
# more examples or you want to see full
# definition, go to:
# https://repl.it/@OndrejLomic/StackO

# also, function can now raise exception,
# e.g. when you try to divide number by
# zero, and it has special effect
# on cards, see last page of tutorial
# for programmers for more info

lambda x: 2 * x
③ 2.2 -> 4.4, 3.5 -> 7, inf -> inf

lambda x: min(x, 11)
③ inf -> 11

def sign
# returns 1 if x > 0, -1 if x < 0
# and 0 when x == 0
③ -0.5 -> -1, 0 -> 0, 57.3 -> 1

def abs
# distance from zero, always positive
③ -1.5 -> 1.5, 0 -> 0, 0.5 -> 0.5\
"""),
  TextHelpCard("red", "", """\
def int_from_list
# "123"[0] == "1", "123"[1] == "2"
② 0 -> 9, 1 -> 5, 12 -> 7
③ 3.1 -> TypeError, inf -> TypeError

def ints_from_list
# "123"[0:1] == "1", "123"[1:3] == "23"
② 0 -> 1, 1 -> 76, 2 -> 781, 3 -> 4
③ 1.1 -> TypeError

lambda x: ceil(sqrt(x))
# sqrt stands for √
③ 4 -> 2, 5 -> 3, -10 -> ValueError

lambda x: floor(log2(x))
# logarithm with base of two
③ 0 -> ValueError, 1 -> 0, 2 -> 1, 3 -> 2

def switch_places
# "{0:.2f}".format(x) always returns x
# to two decimal places (1 / 3 as "3.33",
# -2.5 as "-2.50")
③ 123.456 -> 45.123, -3 -> -0.3

def increment_digits
# "abaa".replace("a", "c") == "cbcc"
# be careful, digit 9 is incremented twice
③ 10 -> 21.11, -9.08 -> -1.19\
"""),
  TextHelpCard("red", "", """\
def reverse
# "abcd"[::-1] == "dcba"
③ 123.5 -> 321, -43 -> -34

def rec_subtract
# beware, this function calls itself!
# rec_s(20) --> rec_s(rec_s(-40)) -->
# rec_s(-40) --> -40 
③ 55 -> -5, -20 -> -20
③ inf -> RecursionError

def rec_divide
③ 1 -> 0, 2 -> 0, 3 -> 1, 10 -> 2
③ -2 -> RecursionError

def double_rec
③ -10 -> 2, 16 -> -1, 260 -> -4
③ inf -> RecursionError

def rec_multiply
③ 1 -> 5, 2 -> 6, -2 -> -10, 1.5 -> 20
③ inf -> inf

# just for sake of sanity, huge numbers
# are interpreted as inf, OverflowError
# does not exist, etc. But if you made it
# this far, you'll manage on your own

# thank you player, have a lot of fun\
"""),
  TextHelpCard("grey", "", 26 * "\n" + """\
     game and design by: Ondřej Lomič
                contact: ondrej@lomic.cz\
""")
]
