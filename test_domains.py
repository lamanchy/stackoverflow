import math
import sys
from time import time

from rules import get_rules
from source_code_helpers import get_source_code_name
from values import values


def get_result(rule, value):
  try:
    value = rule(value)
    value = round(value, 5)
    if value == int(value): value = int(value)
    return value
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
    return "white-inf"

  try:
    if int(value) == value:
      value = int(value)  # 0.0 to 0 etc
  except ValueError:
    return "white-NaN"
  except OverflowError:
    return "white-inf"

  if isinstance(value, int):
    if 0 < value < 21:
      return "green-int"

    if -20 <= value <= 100:
      if value < 0: return "yellow-int-"
      return "yellow-int+"

    if -200 <= value <= 200:
      if value < 0: return "red-int-"
      return "red-int+"

    if value < 0: return "white-int-"
    return "white-int+"

  if (int(value * 100) % 10) == 0 or \
      value % (1 / 8) < 0.001 or \
      (int(value * 10) % 10) == (int(value * 100) % 10):

    if value < 0: return "red-float-"
    return "red-float+"

  if value < 0: return "white-float-"
  return "white-float+"


def view_results():
  colors = ["green", "yellow", "red"]
  for num in range(2, 3):
    print("stats with %s cards" % (num + 1))
    print()
    # for c in range(len(colors)):
    for c in [2]:
      print(colors[:c + 1])
      color_values = []
      color_rules = []
      for color in colors[:c + 1]: color_values += values[color]
      for color in colors[:c + 1]: color_rules += get_rules()[color]
      color_values = [v[0] for v in color_values]
      color_values.sort()

      total = {}
      fn_total = {}
      s = [0]
      fn_s = {}
      value_color_fns = {}
      total_values = {}

      def account(_value, *rules):
        _rule = rules[0]
        original = _value
        time_start = time()
        for _rule in rules:
          _value = get_result(_rule, _value)
          if get_value_color(_value).split('-')[0] not in colors:
            break
        if time() - time_start > .01:
          print("\n", time() - time_start, original, [get_source_code_name(fn)[0] for fn in rules], _value)

        result_color = get_value_color(_value)
        if result_color not in total:
          total[result_color] = 0
        total[result_color] += 1
        s[0] += 1

        if result_color not in value_color_fns:
          value_color_fns[result_color] = []
        if _rule not in value_color_fns[result_color]:
          value_color_fns[result_color].append(_rule)

        if _rule not in fn_total: fn_total[_rule] = {}
        if _rule not in fn_s: fn_s[_rule] = 0
        if _value not in fn_total[_rule]:
          fn_total[_rule][_value] = 0
        fn_total[_rule][_value] += 1
        fn_s[_rule] += 1

        if _value not in total_values:
          total_values[_value] = 0
        total_values[_value] += 1

      for val_num, value in enumerate(color_values):
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
        print(int(val_num / len(color_values) * 100), end="% ")
        sys.stdout.flush()
      print()

      for color, count in sorted(total.items(), key=lambda w: (-w[1], w[0])):
        print('{:20}'.format(color), end=': ')
        print("{: 6.2f}%".format(100 * count / s[0]), end='')
        print('{}'.format("(abs count = "), end='')
        print('{:6}'.format(count), end=' out of ')
        print('{:6}'.format(s[0]), end=')\n')

      # if num == 0 and len(colors[:c + 1]) == 4:
      for rule, _ in sorted(fn_total.items(), key=lambda ww: -sorted(ww[1].items(), key=lambda w: -w[1])[0][1]):
        print("fn:", get_source_code_name(rule)[0])
        for color, count in sorted(fn_total[rule].items(), key=lambda w: -w[1])[:5]:
          print('{:20}'.format(color), end=': ')
          print("{: 6.2f}%".format(100 * count / fn_s[rule]), end='')
          print('{}'.format("(abs count = "), end='')
          print('{:6}'.format(count), end=' out of ')
          print('{:6}'.format(fn_s[rule]), end=')\n')
        print()

      print("fns which produced certain result:")
      for value_color in value_color_fns:
        print("{:20}".format("color: " + value_color), [get_source_code_name(fn)[0] for fn in value_color_fns[value_color]])

      print()

      print("most common values globally:")
      for value, count in sorted(total_values.items(), key=lambda w: -w[1])[:40]:
        print("{:20}".format("value: " + str(value)), count / s[0] * 100)
    print()
    print()


if __name__ == "__main__":
  view_results()
