import math

from generate_pdf import get_source_code
from rules import get_rules
from values import values


def get_result(rule, value):
  try:
    if value == math.inf:
      value = 1000000000000000000000000000000000000000
    return rule(value)
  except ZeroDivisionError:
    return 'zd'
  except ValueError:
    return 've'
  except TypeError:
    return 'te'
  except RecursionError:
    return 're'
  except OverflowError:
    return math.inf


def get_value_color(value):
  if isinstance(value, str):
    return value

  if value == math.inf:
    return "black-inf"

  if isinstance(value, int):
    if 0 < value < 21:
      return "green-int"

    if -20 <= value <= 100:
      if value < 0: return "yellow-int-"
      return "yellow-int+"

    if -200 <= value <= 200:
      if value < 0: return "red-int-"
      return "red-int+"

    if value < 0: return "black-int-"
    return "black-int+"

  if (int(value * 100) % 10) == 0 or \
      value % (1 / 8) < 0.001 or \
      (int(value * 10) % 10) == (int(value * 100) % 10):

    if value < 0: return "red-float-"
    return "red-float+"

  if value < 0: return "black-float-"
  return "black-float+"


def view_results():
  colors = ["green", "yellow", "red", "black"]
  for num in range(3):
    print("stats with %s cards" % (num + 1))
    print()
    for c, color in enumerate(colors):
      print(colors[:c + 1])
      color_values = []
      color_rules = []
      for color in colors[:c + 1]: color_values += values[color]
      for color in colors[:c + 1]: color_rules += get_rules()[color]
      color_values = [v[0] for v in color_values]
      color_values.sort()

      total = {}
      s = [0]
      def account(value, *fns):
        for fn in fns:
          value = get_result(rule, value)
          if get_value_color(value) not in colors:
            break

        result_color = get_value_color(value)
        if result_color not in total:
          total[result_color] = 0
        total[result_color] += 1
        s[0] += 1

      for value in color_values:
        for i, rule in enumerate(color_rules):
          for i2, rule2 in enumerate(color_rules):
            if num == 0: break
            if i == i2: continue
            for i3, rule3 in enumerate(color_rules):
              if num == 1: break
              if i == i3 or i2 == i3: continue
              for i4, rule4 in enumerate(color_rules):
                if num == 2: break
                if i == i4 or i2 == i4 or i3 == i4: continue
                account(value, rule, rule2, rule3, rule4)
              account(value, rule, rule2, rule3)
            account(value, rule, rule2)
          account(value, rule)

      for color, count in sorted(total.items(), key=lambda w: (-w[1], w[0])):
        print('{:20}'.format(color), end=': ')
        print("{: 6.2f}%".format(100 * count / s[0]), end='')
        print('{}'.format("(abs count = "), end='')
        print('{:6}'.format(count), end=' out of ')
        print('{:6}'.format(s[0]), end=')\n')

    print()
    print()


if __name__ == "__main__":
  view_results()
