from cards.text_help_card import TextHelpCard
from cards.title_help_card import TitleHelpCard

red_tutorial = [
  TitleHelpCard("How to play\nthis game", "(tutorial for programmers)", "red"),
  TextHelpCard("red", "", """\
# DON'T PANIC

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
"""),

  # for font 15
  #  MAX LINE LENGTH 29 SIGNS!!
  #  MAX FUNCTION LINES 21 !!!!

  # for font 11
  #  MAX LINE LENGTH 41 SIGNS!!!!!!!!!!!!!!
  #  MAX FUNCTION LINES 29 !!!!!!!!!!!!!!!!
  TextHelpCard("red", "", """\
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

  # functions' back is orange
  global function_deck = [
    card for card in cards
      if card.back_color == "orange"]

  # you wont need the rest of the cards
  # until next game with different
  # difficulty\
"""),
  TextHelpCard("red", "", """\
def prepare_game():
  # shuffle both decks separately
  # (prepared in select_difficulty func)
  shuffle(values_deck)
  shuffle(function_deck)

  # select one output value from the top
  # of value_deck, it stays the same
  # for a whole game
  global output_value = values_deck.pop()

  # this game is for two or more players
  players_num = input("Enter number "
     "of players, 2 or more")
  global players = []

  # at the beginning of game, each player
  # gets 4 func. cards from function_deck
  for _ in range(players_num):
    players.append([function_deck.pop() 
                      for i in range(4)])

# now you are ready to play the first
# round of game\
"""),
  TextHelpCard("red", "", """\
def nobody_won():
  # if some player has no function cards
  # in hand, the game ends
  return all([len(funcs) > 0
                for funcs in players])


def play_round():
  # get one input value (only for this
  # round) from the top of value_deck
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
"""),
  TextHelpCard("red", "", """\
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
"""),
  TextHelpCard("red", "", """\
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
    # try to divide with zero, which
    # causes player to loose round and
    # has additional effect described
    # in handle exception function 
    except Exception as e:
      handle_exception(i, e)
      res[i] = inf

  return res\
"""),
  TextHelpCard("red", "", """\
def get_winners(computed_values):
  # determine distances between players'
  # computed values and output value
  distances = [
    abs(output_value - value)
      for value in computed_values]

  # all players with a distance equal to
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
  # point, use shuffled used func. cards\
"""),
  TextHelpCard("red", "", """\
# exceptions never occur on green 
# difficulty and rarely on a yellow one 
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
""")]

for card in red_tutorial:
  card.is_upside_down = True
  card.should_resize = True
