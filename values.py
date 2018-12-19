from math import *

values = {
    "green": range(1, 21),
    "yellow": [-20, -15, -10, -5, -4, -3, -2, -1, 0, 22, 25, 30, 35, 40, 42, 50, 66, 80, 99, 100],
    "red": [-200, -144, -110, -100, -66, -30, 120, 150, 169, 199, 200, 1 / 2, 3 / 4, -5 / 6, 6.6, -1 / 8, 5 / 7, -3 / 2,
            10.1, -0.1],
    "grey": [pi, e, 0.99, 1024, sqrt(2), -17.76],
}


def get_all_values():
    fns = []
    for color in values:
        for fn in values[color]:
            fns.append((fn, color))

    return fns


if __name__ == "__main__":
    for color in values:
        print(color, len(values[color]), values[color])
