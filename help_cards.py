
# for font 15
#  MAX LINE LENGTH 29 SIGNS!!
#  MAX FUNCTION LINES 21 !!!!

# for font 11
#  MAX LINE LENGTH 41 SIGNS!!!!!!!!!!!!!!
#  MAX FUNCTION LINES 29 !!!!!!!!!!!!!!!!

help_cards = [
  """\
HOW TO PLAY THIS GAME 1
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
    play_round()

# when somebody wins, game
# ends\
""",
  """\
HOW TO PLAY THIS GAME 5
def select_cards():
  # each player selects one or more
  # function cards from hand
  selected = []
  for cards in players:
    to_use = input("Enter indicies of "
                "function cards to use")

    selected.append([cards[i]
                     for i in
                     to_use.split(", ")])

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
HOW TO PLAY THIS GAME 2
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
HOW TO PLAY THIS GAME 6
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
HOW TO PLAY THIS GAME 3
def prepare_game():
  # shuffle both decks (prepared 
  # in select_difficulty function)
  shuffle(values_deck)
  shuffle(function_deck)

  # select output value form the top
  # of value deck, it stays the same
  # for whole game
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
HOW TO PLAY THIS GAME 7
def get_winners(computed_values):
  # determine distances between computed
  # values and output value
  distances = [
    abs(output_value - value)
      for value in computed_values]

  # get minimum distance
  min_distance = min(distances)

  # all players with distance equal to
  # minimum distance win the round
  return [i for i in range(players)
    if distances[i] == min_distance]


def get_new_functions(selected, winners):
  # each player gets as many function
  # as he used, only winners get one 
  # function card less
  for i, cards in players:
    to_get = len(selected[i])
    if i in winners:
      to_get -= 1

    for _ in range(to_get):
      cards.append(function_cards.pop())\
""",
  """\
HOW TO PLAY THIS GAME 4
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

  # based on input value and computed
  # values (and global output value),
  # winners of this round are determined
  winners = get_winners(values)

  # all players get new function cards,
  # winners get one less
  get_new_functions(selected, winners)\
""",
  """\
HOW TO PLAY THIS GAME 8
# exceptions occur rarely 
# at easy difficulty
def handle_exception(i, ex):
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
      cards += [function_deck.pop()]

  # sqrt(-2) or log2(0) raises ValueError
  if isinstance(ex, ValueError):
    # input value is changed, before
    # computation of winners
    input_value = value_deck.pop()

  # anything divided by zero...
  if isinstance(ex, ZeroDivisionError):
    # output value is changed
    output_value = value_deck.pop()\
""",
  """\
HOW TO USE A FUNCTION (OR MORE)
fn1 = lambda x: x + 5

fn1(3) == (3+5) == 8
#        3 == input
#        ↓
# lambda 3: 3 + 5
#             ↓
#             8 == output
fn1(4) == (4+5) == 9 
fn1(1) == (1+5) == 6 


fn2 = lambda x: x * 2

fn1(fn2(2)) = (2*2)+5 == 9 
#
#        3 == input
#        ↓
# lambda 2: 2 * 2
#             ↓
#             4
#             ↓
#      lambda 4: 4 + 5
#                  ↓
#        output == 9
fn2(fn1(2)) == (2+5)*2 == 14
fn2(fn1(3)) == (3+5)*2 == 16
fn2(fn2(3)) == (3*2)*2 == 12\
""",
  """\
# HOW SOME MYSTERIOUS THINGS WORK:

5 // 3 == 1 and -5 // 3 == -2
5 / 3 == 1.6666666666666666
5 % 3 == 2  and -5 % 3 == 1
round(0.4) == 0 and round(0.5) == 1
floor(0.7) == 0 and ceil(0.2) == 1
"asd"[1] == "s" and "asd"[0:2] == "as"
"asd"[-1] == "d" and "asd"[::-1] == "dsa"\
""",
  """\
# HOW SOME MYSTERIOUS THINGS WORK (part 2):

def gcd(a, b):  # greatest common divisor
  while b > 0: a, b = b, a % b
  return a
def lcm(a, b): return abs(a * b) // gcd(a, b)
def is_prime(n):
  if n != int(n):  return False
  if n <= 1:       return False
  for i in range(2, n):
      if (n % i) == 0: return False
  return True\
""",
  """\
# basic functions:
# +=
x = 1   # x has a value of 1
x += 3  # value 1 was added to x
x == 4  # value of x is equal to 4
x -= 2  # 2 is subtracted from x
x == 2  # value of x is equal to 2
x *= 3  # x is multiplied by 3
x == 4  # x is equal to 4

# >= > <= < ==
3 > 2 == True
2 <= 2 == True
5 < 3 == False
(1 == 2) == False

# /
# division without rounding
5 / 2 == 2.5
- 5 / 2 == -2.5

# //
# division with rounding
a // b == floor(a / b)  # see fn floor lower
5 // 3 == 1
- 5 // 3 == - 2

# round, floor, ceil
floor(2.9) == 2    # floor always down
floor(-1.5) == -2
ceil(1.1) == 2     # ceil always up
round(2.49) == 2   # round to closest (0.5 up)
round(2.5) == round(3.49) == 3

# %
# remainder (even for not whole numbers)
5 % 3 == 8 % 3 == 2
- 5 % 3 == 4 % 3 == 1
1.4 % 0.3 == 0.2
- 1.4 % 0.3 == 0.1

# min, max
min(2, 7) == 2
min(20, -3) == -3
max(2, -10) == 2

# gcd, lcm
# greatest common divisor, least common multiple
def gcd(a, b):
  while abs(b) > 0:
    a, b = b, a % b
  return abs(a)

def lcm(a, b):
  return abs(a * b) // gcd(a, b)\
"""
]


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
