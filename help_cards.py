
# for font 15
#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 21 !!!!

# for font 11
#  MAX LINE LENGTH 41 SIGNS!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 29 !!!!!!!!!!!!!!!!
from rules import get_all_functions

help_cards = [
  """\
# HOW TO PLAY THIS GAME 1
# DONT'T PANIC

# read comments (grey text),
# it's gonna be ok
def game():
  # firstly select difficulty
  select_difficulty()
  # (find card with function
  # "select_difficulty", that
  # will tell you, how to do
  # that)

  # then prepare the game
  prepare_game()
  # this is done once at the
  # beginning of each game
    
  # play round as long
  # as nobody has won
  while nobody_won():  
    play_round()\
""",
  """\
# HOW TO PLAY THIS GAME 5
def select_cards():
  # each player selects one or more
  # function cards from hand
  selected = []
  for cards in players:
    to_use = input("Enter indicies of "
                "function cards to use")

    selected.append([cards[i]
            for i in to_use.split(", ")])

  # after all players selected function
  # cards to play, show them to others
  for i, cards in enumerate(selected):
    for card in cards:
      players[i].remove(card)
      # ala remove card from your hand :)

  return selected\
""",

# for font 15
#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 21 !!!!

# for font 11
#  MAX LINE LENGTH 41 SIGNS!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 29 !!!!!!!!!!!!!!!!
  """\
# HOW TO PLAY THIS GAME 2
def select_difficulty():
  difficulty = input("Enter number 1-4, "
    "1 is the easiest difficulty")

  colors = ["green", "yellow",
            "red", "white"][:difficulty]
  # at easiest difficulty, you play only
  # with green cards, at difficulty 2,
  # you play with green and yellow
  # cards... so select only cards
  # with matching face color:
  cards = [
    card for card in get_all_cards()
      if card.face_color in colors]

  # values are cards with blue back
  global values_deck = [
    card for card in cards
      if card.back_color == "blue"]
      
  # correspondingly select functions
  global function_deck = [
    card for card in cards
      if card.back_color == "orange"]
  
  # you wont need the rest of the cards
  # until next game with different
  # difficulty\
""",
  """\
# HOW TO PLAY THIS GAME 6
def compute_outputs(selected):
  # first card transforms input value to
  # a different one, second (third...)
  # card transforms already transformed
  # value
  # for more info see help card HOW TO
  # USE FUNCTIONS
  # be careful, order matters!
  res = [input_value for _ in players]
  for i, cards in enumerate(selected):
    try:
      for function_card in cards:
        res[i] = function_card(res[i])

    # rarely, at higher difficulty,
    # exception can happen, e.g. when you
    # try to divide with zero
    except Exception as e:
      handle_exception(i, e)
      res[i] = inf

  return res\
""",
  """\
# HOW TO PLAY THIS GAME 3
def prepare_game():
  # shuffle both decks (prepared 
  # in select_difficulty function)
  shuffle(values_deck)
  shuffle(function_deck)

  # select output value from the top
  # of value deck, it stays the same
  # for a whole game
  global output_value = values_deck.pop()
  
  # how many players are playing?
  players_num = input("Enter number "
     "of players, 2 or more")
  global players = []

  # at the beginning of game, each player
  # gets 4 fn cards from function_deck
  for _ in range(players_num):
    players.append([function_deck.pop() 
                      for i in range(4)])
  
# now you are ready to play the first
# round of game\
""",
  """\
# HOW TO PLAY THIS GAME 7
def get_winners(computed_values):
  # determine distances between computed
  # values and output value
  distances = [
    abs(output_value - value)
      for value in computed_values]

  # all players with distance equal to
  # minimum distance win the round
  winners = [i for i in range(players)
    if distances[i] == min(distances)]

  return winners


def get_new_functions(selected, winners):
  # each player gets as many function
  # as he used, only winners get one 
  # function card less
  for i, cards in players:
    to_get = len(selected[i])
    if i in winners:
      to_get -= 1

    for _ in range(to_get):
      cards.append(function_deck.pop())

  # if function_deck gets empty at any
  # point, use shuffled used fn cards\
""",
  """\
# HOW TO PLAY THIS GAME 4
def nobody_won():
  # if any player has no function cards
  # in hand, the game ends
  return all([len(fns) > 0
                for fns in players])


def play_round():
  # get input value (only for this round)
  # from the top of value deck
  global input_value = value_deck.pop()

  # all players select function card(s)
  # from their hand, which they will use
  selected = select_cards()
  
  # based on selected cards, determine 
  # computed value for each player
  values = compute_outputs(selected)

  # based on input value, output_value
  # and computed values, winners of this
  # round are determined
  winners = get_winners(values)

  # all players get new function cards,
  # winners get one less
  get_new_functions(selected, winners)\
""",
  """\
# HOW TO PLAY THIS GAME 8
# exceptions occur rarely 
# at easy difficulty
def handle_exception(i, ex):
  # sqrt(-2) or log2(0) raises ValueError
  if isinstance(ex, ValueError):
    # input value is changed, before
    # computation of winners
    input_value = value_deck.pop()

  # anything divided by zero...
  if isinstance(ex, ZeroDivisionError):
    # output value is changed
    output_value = value_deck.pop()
    
  # TypeError is raised, e.g. when you
  # try to get 2.5th item of a list
  if isinstance(ex, TypeError):
    # player, who raised TypeError, gets
    # one extra function card
    players[i] += [function_deck.pop()]

  # RecursionError is raised, when there
  # is no end to recursion
  if isinstance(ex, RecursionError):
    # all players get extra function card
    for cards in players:
      cards += [function_deck.pop()]\
""",
  """\
# HOW TO USE A FUNCTION
fn1 = lambda x: x + 5
fn1(3) == (3+5) == 8
#        3 == input
#        ↓
# lambda 3: 3 + 5
#             ↓
#             8 == output
fn1(4) == (4+5) == 9 
fn1(1) == (1+5) == 6 

def fn2(x):
 return x * 2

fn2(2) == (2*2) == 4
fn1(fn2(2)) == (2*2)+5 == 9 
#
#        2 == input
#        ↓
#    fn2(2):
#      return 2 * 2
#               ↓
#               4
#               ↓
#        lambda 4: 4 + 5
#                    ↓
#          output == 9
fn2(fn1(2)) == (2+5)*2 == 14
fn2(fn1(3)) == (3+5)*2 == 16
fn2(fn2(3)) == (3*2)*2 == 12\
""",
  """\
# HELP FOR š CARDS 1
# just a reminder, some combinations
# of cards might get ugly results, so
# if you cannot calculate something
# in your head, then just dont use it

lambda x: x // -6
# x // y is eqivalent to floor(x / y),
# floor rounds down
š 0 -> 0, 1 -> -1, 6 -> -1, 7 -> -2
č 6.1 -> -2

lambda x: 100 // x
š 3 -> 33, -5 -> -20
č -3.3 -> -30

lambda x: ceil(sqrt(abs(x)))
# sqrt == √, abs(3) == abs(-3) == 3
š 4 -> 2, 16 -> 4, -10 -> 4

lambda x: floor(log2(abs(x)))
š 0 -> ValueError, 1 -> 0, 2 -> 1, 4 -> 2

lambda x: sin(pi * x / 2) - 2
š 0 -> -2, 1 -> -1, 2 -> -2, 3 -> -3
č 2.2 -> #metoo
ř inf -> ValueError

def if_greater_or_less
š 0 -> 66, 5 -> 42, 42 -> 42, 99 -> 5\
""",
  """\
# PROGRAM STATEMENTS (IF, FOR, WHILE)
def if_fn(x):
  if x > 3:
    x += 1
    # this is executed only if condition
    # is true (x is bigger then 3)
  elif x < 1:
    x += 2
    # this is exectued only if previous
    # if condifiton is false, and this
    # condition is true
  else:
    x += 3
    # this is executed if both previous
    # conditions are false
  return x + 10 # this is executed always

if_fn(4) == 15 and if_fn(0) == 12
if_fn(2) == 15

if x > 3: x = 1 # one line eqivalent of
                # the first if statement

while x > 0: x -= 1
# x -= 1 is executed over and over,
# as long as x is bigger than zero

for _ in range(num):
  x -= 1 # this statement is executed
         # num-times\
""",
  """\
# HELP FOR š CARDS 2
def if_equal_or_not
š 10 -> 76, 20 -> 10, 66 -> 6

def for_cycle  # see PROGRAM STATEMENTS
š 0 -> 0, 1 -> 11, 9 -> 44, 10 -> 10

def while_cycle
š 2 -> 2, 5 -> 2, 3 -> 0, 11 -> 4
č 2.2 -> 0, -4.9 -> -2

def int_from_list
# "abc"[0] == "a", "abc"[1] == "b"
š 0 -> 9, 1 -> 5, 12 -> 7
č 3.1 -> TypeError
ř inf -> TypeError

def ints_from_list
# "abc"[0:1] == "a", "abc"[0:2] == "ab"
š 0 -> 1, 1 -> 76, 2 -> 781, 3 -> 4
č 1.1 -> TypeError

def split_by_int
# "abac".split("a") == ["", "b", "c"]
# len(list) == number of items in list
š 0 -> -3, 2 -> -1, 7 -> -2

def last_digit
# -1 takes last item from list
š 2 -> 2, 31 -> 1, -23 -> 3\
""",
  """\
# HELP FOR ě CARDS 1
lambda x: 15
# constant function, it returns 15 for
# any input value
ě 1 -> 15, -2 -> 15
# 1 -> 15 is an example, this function
# for input value 1 returns value 15
# green sign ě shows, that this example
# is relevant for green difficulty, you
# can ignore examples for higher
# difficulties than you play

lambda x: x
ě 1 -> 1, 2 -> 2, 12 -> 12

lambda x: x + 5
ě 1 -> 6, 7 -> 12

lambda x: 2 * x
ě 1 -> 2, 3 -> 6
š 0 -> 0, -2 -> -4
č 2.2 -> 4.4, 3.5 -> 7

lambda x: min(x, 11)
ě 1 -> 1, 11 -> 11, 16 -> 11
ř inf -> 11

lambda x: ceil(x / 3)  # ceil rounds up
ě 1 -> 1, 2 -> 1, 3 -> 1, 4 -> 2
š -3 -> -1, -2 -> 0, 0 -> 0\
""",
  """\
# HELP FOR č CARDS
# well, functions might get bit tricky
# down the road, so if you are in need of
# more examples or you want to see full
# definition, go to:
# https://repl.it/@OndrejLomic/StackO

def switch_places
# sign(x) return 1 if x > 0, -1 if x < 0
# and 0 if x == 0
# "{0:.2f}".format(x) always returns x
# to two decimal places
č 123.456 -> 45.123, -3 -> -0.3

def put_and_eval
# eval("2-1") executes string as if it
# was python, returning 1
č 1.1 -> 0, -2.3 -> 5, 0.5 -> -5

def reverse
# "abcd"[::-1] == "dcba"
č 123.5 -> 321, -43 -> -34

def subtract_madness
# '-'.join("123") == "1-2-3"
č 1 -> 1, 1.1 -> 0, 1.11 -> -1, 2.1 -> 1
ř inf -> ValueError\
""",
  """\
# HELP FOR ě CARDS 2
lambda x: max(x, 9)
ě 1 -> 9, 10 -> 10

lambda x: gcd(x, 24)
# greatest common divisor
ě 10 -> 2, 12 -> 12, 16 -> 8
š 0 -> 24, -5 -> 1
č 1.5 -> 1.5, -3.5 -> 0.5
ř √2 -> ValueError, inf -> 24

lambda x: lcm(x, 6)
# lowest common multipler
ě 2 -> 6, 8 -> 24, 7 -> 42
š 0 -> 0, -5 -> 30
č 1.5 -> 6, 2.5 -> 30
ř √2 -> ValueError, inf -> inf

lambda x: (x % 5) + 1  # remainder
ě 1 -> 2, 7 -> 3, 10 -> 1
š -2 -> 4, -9 -> 2
č 5.5 -> 1.5, -9.5 -> 1.5
ř inf -> 1

def if_prime
# find definition on card
ě 1 -> 1, 2 -> 17, 4 -> 4, 5 -> 17
č 0 -> 0, -5 -> -5
ř 200 -> 200, 201 -> 0, 0.5 -> 0.5\
""",
  """\
# HELP FOR č and ř CARDS
def rec_subtract
# beware, this function calls itself!
č 55 -> -5

def rec_divide
č 1 -> 0, 2 -> 1, -4 -> -1, -5 -> -2
ř inf -> RecursionError

def double_rec
č -10 -> 2, 16 -> -1, 260 -> -4
ř inf -> RecursionError

def rec_multiply
č 1 -> 5, 2 -> 6, -2 -> -10, 1.5 -> 20
ř π -> inf, inf -> inf

def ack # no help for you, you can 
        # figure it out, i believe in you

def fibb      # i warned you, don't use
ř 2.5 -> 0.5  # it if you can't handle it

# just for sake of sanity, huge numbers
# are interpreted as inf, OverflowError
# does not exist etc. But if you made it
# this far, you'll manage on your own.

# thank you player, and have a lot of fun
#                                     B.\
"""]


def get_all_help_cards():
  tmp = []
  help = []
  for i, card in enumerate(help_cards):
    tmp.append(card)

    if i + 1 == len(help_cards) or len(tmp) == 2:
      if len(tmp) == 1:
        tmp.append("")

      help.append(tuple(tmp))
      tmp = []

  return help


if __name__ == "__main__":
  for fn, color in get_all_functions():
    print(color, fn)
