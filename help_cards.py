help_cards = [
    """\
# HOW TO PLAY THIS GAME:
def game():
    # at fist prepare the game:
    prepare_game()
    
    # play round as long as nobody has won
    while nobody_won():
        play_round()


# game preparation is on the other side...\
""",
    """\
# do this at the beginning of each game
def prepare_game():
    # select output value, it is the same
    # for whole game
    global output_value = pop_random_value()
    
    # each player gets 5 function cards
    global players = []
    for _ in range(len(players)):
        players.append(
            [pop_random_fn() for i in range(4)]
        )\
""",
    """\
def nobody_won():
    # if any player has 0 functions, the game has ended
    return all(
        [len(cards) > 0 for cards in players]
    )\
""",
    """\
def play_round():
    input_value = pop_random_value()
    # TODO
    # each player selects some functions,
    # to transform input value to output value
    # as close as possible, the one with closest
    # value is a winner. Used functions are put
    # away, each player gets as many new functions
    # as he used, only winner gets one less.\
""",
    """\
# HOW TO USE FUNCTION:
# function: lambda x: x + 5
    
# input value: 3 
#              ↓
#       lambda 3: 3 + 5
#                   ↓
#     output value: 8\
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
