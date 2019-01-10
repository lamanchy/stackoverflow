from math import *

values = {
  "green": [1, 2, 3, 4, 6, 8, 9, 5, 11, 12, 14, 10, 16, 17, 18, 20],  # 2-5
  "yellow": [-20, -16, -8, -5, -4, -3, -2, -1, 0, 22, 27, 30, 33, 40, 42, 49, 66, 81, 99, 100],  # 6-10
  "red": [-200, -144, -66, 121, 169, 199, (1 / 2, "1/2"), 6.6, (-1 / 8, "-1/8"), (-3 / 2, "-3/2"),
          -0.1, 10.1],  # 12 KQJ
  "black": [(pi, "π"), 1024, (sqrt(2), "√2"), -17.76],  # 4 esa
}

for c in values:
  for i, v in enumerate(values[c]):
    if not isinstance(v, tuple):
      values[c][i] = v, "{0:.2f}".format(v).rstrip('0').rstrip('.')


def get_all_values():
  fns = []
  for color in ["green", "yellow", "red", "black"]:
    # for color in ["green", "yellow"]:
    for fn in values[color]:
      fns.append((fn, color))

  return fns


if __name__ == "__main__":
  for color in values:
    print(color, len(values[color]), values[color])
