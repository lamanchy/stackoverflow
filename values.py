from math import *

values = {
    "green": range(1, 21),
    "yellow": [-20, -15, -10, -5, -4, -3, -2, -1, 0, 22, 25, 30, 35, 40, 42, 50, 66, 80, 99, 100],
    "red": [-200, -144, -110, -100, -66, -30, 120, 150, 169, 199, 200, 1 / 2, 3 / 4, -5 / 6, 6.6, -1 / 8, 5 / 7, -3 / 2,
            10.1, -0.1],
    "black": [pi, e, 0.99, 1024, sqrt(2), -17.76],
}

if __name__ == "__main__":
    for color in values:
        print(color, len(values[color]), values[color])

