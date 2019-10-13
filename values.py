from cards.playing_card_back import PlayingCardBack
from cards.two_sided_card import TwoSidedCard
from cards.value_card import ValueCard

values = {
  "green": [1, 2, 3, 4, 5, 8, 10, 11, 12, 14, 16, 17, 18, 20],  # 2-5 14 only!
  "yellow": [-10, -5, -4, -3, -2, -1, 0, 21, 22, 24, 25, 27, 30, 33, 35, 40, 42, 50],  # 6-10
  "red": [-20, -15, -12, 60, 75, 81, 90, 100, (1 / 2, "0.5"), 5.5, (-1 / 8, "-0.125"), (-3 / 2, "-1.5"),
          -0.1, 10.1, (99.9, "99.9"), (-15.1, "-15.1")],  # 16 KQJ
  # "white": [(pi, "π"), 1024, (sqrt(2), "√2"), -17.76],  # 4 esa
}

for c in values:
  for i, v in enumerate(values[c]):
    if not isinstance(v, tuple):
      values[c][i] = v, "{0:.2f}".format(v).rstrip('0').rstrip('.')


def get_all_values():
  vals = []
  for c in ["green", "yellow", "red"]:
    # for color in ["green", "yellow"]:
    for value in values[c]:
      vals.append(TwoSidedCard(ValueCard(c, value), PlayingCardBack("blue")))

  return vals


if __name__ == "__main__":
  for color in values:
    print(color, len(values[color]), values[color])
