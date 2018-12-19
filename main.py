from rules import get_rules
from values import values


def get_result(rule, value):
    try:
        return int(rule(value))
    except ZeroDivisionError:
        return 'zd'
    except ValueError:
        return 'te'


def view_results():
    colors = ["green", "yellow", "red", "grey"]
    for c, color in enumerate(colors):
        print(colors[:c + 1])
        print('r', end='\t')
        color_values = []
        color_rules = []
        for color in colors[:c + 1]: color_values += values[color]
        for color in colors[:c + 1]: color_rules += get_rules()[color]
        color_values = [v[0] for v in color_values]
        color_values.sort()
        for value in color_values:
            print(value, end='\t')
        print()

        for i, rule in enumerate(color_rules):
            print(i, end='\t')
            for value in color_values:
                print(get_result(rule, value), end='\t')
            print()


if __name__ == "__main__":
    view_results()
