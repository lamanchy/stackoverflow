from math import inf
from random import shuffle


class Card(object):
  face_color = "green"
  back_color = "blue"


def get_all_cards(): return []


value_deck = []
function_deck = []
input_value = None
output_value = None
players = []


def play_game():
  select_difficulty()

  prepare_game()
  while nobody_won():
    play_round()


def select_difficulty():
  global value_deck, function_deck
  difficulty = int(input("Enter number 1-4, 1 is the easiest difficulty"))

  colors = ["green", "yellow", "red", "white"][:difficulty]

  cards = [card for card in get_all_cards() if card.face_color in colors]

  value_deck = [card for card in cards if card.back_color == "blue"]
  function_deck = [card for card in cards if card.back_color == "orange"]


def prepare_game():
  shuffle(value_deck)
  shuffle(function_deck)

  global output_value
  output_value = value_deck.pop()

  players_num = int(input("Enter number of players, 2 or more"))

  players.append = [
    [
      function_deck.pop() for _ in range(4)
    ] for _ in range(players_num)
  ]


def nobody_won():
  return all([len(funcs) > 0 for funcs in players])


def play_round():
  global input_value
  input_value = value_deck.pop()

  selected = select_cards()

  values = compute_outputs(selected)

  winners = get_winners(values)

  get_new_functions(selected, winners)


def select_cards():
  selected = []
  for cards in players:
    to_use = input("Enter indicies of function cards to use")

    selected.append([cards[i] for i in to_use.split(", ")])

  for i, cards in enumerate(selected):
    for card in cards:
      players[i].remove(card)

  return selected


def compute_outputs(selected):
  res = [input_value for _ in players]
  for i, cards in enumerate(selected):
    try:
      for function_card in cards:
        res[i] = function_card(res[i])

    except Exception as e:
      handle_exception(i, e)
      res[i] = inf

  return res


def get_winners(computed_values):
  distances = [abs(output_value - value) for value in computed_values]

  winners = [i for i in range(players) if distances[i] == min(distances)]

  return winners


def get_new_functions(selected, winners):
  for i, cards in players:
    to_get = len(selected[i])
    if i in winners:
      to_get -= 1

    for _ in range(to_get):
      cards.append(function_deck.pop())


def handle_exception(i, ex):
  global input_value, output_value
  if isinstance(ex, ValueError):
    input_value = value_deck.pop()

  if isinstance(ex, ZeroDivisionError):
    output_value = value_deck.pop()

  if isinstance(ex, TypeError):
    players[i] += [function_deck.pop()]

  if isinstance(ex, RecursionError):
    for cards in players:
      cards += [function_deck.pop()]


if __name__ == "__main__":
  play_game()