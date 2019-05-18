from cards.picture_help_card import PictureHelpCard
from cards.text_help_card import TextHelpCard
from cards.title_help_card import TitleHelpCard
from help.picture_generation import get_first_image, get_play, get_first_chain_image, get_second_chain_image

green_tutorial = [
  TitleHelpCard("How to play\nthis game", "(tutorial for mortals)", "green"),
  TextHelpCard("green", "## Hello to Stack Overflow", """\
# If you wanna jump to playing the game,
# don't worry, go ahead. But if you are't
# in hurry, there are few lines for you:

# This game is hard. Well, not difficult,
# at least not at the easiest difficulty,
# even my 11 years old sister-in-law can
# play it. But I'll warn you, you'll have
# to use your head. A lot.

# Furthermore, even learning this game can
# be a bit of challenge, maybe not so much
# for a skilled programmer, but if you've
# forgotten, what prime is, you will learn
# a thing or two. Programming, for
# example. Well, not all of it, but..
# the important stuff, I would say.

# And at the end, there's feeling like no
# other, not when you win by a luck, but
# by your knowledge and skill. When
# victory is deserved, it tastes sweeter.

# I hope you'll have fun.
#                                     B.\
"""),
  PictureHelpCard("green", "## Firstly select a difficulty", """\
# Find all cards with green face (that's
# the easiest difficulty), then split
# the cards by back color, values are blue
# and functions are orange.\
""",
                  lambda: get_first_image()
                  ),
  PictureHelpCard("green", "## Before each game", """\
# Select output value, from value deck.
# Each player gets 4 functions.
# 
# Game is prepared, now play rounds
# as long as nobody wins.\
""",
                  lambda: get_play(
                    fns_count=8,
                    values_count=13,
                    input_value_index=None,
                    output_value_index=7,
                    used_fn_indexes=[],
                    front_hand_count=4,
                    right_hand_count=4
                  )
                  ),
  PictureHelpCard("green", "## Select new input value", """\
# There is a new input value each round,
# output value stays the same
# for a whole game\
""",
                  lambda: get_play(
                    fns_count=8,
                    values_count=12,
                    input_value_index=3,
                    output_value_index=7,
                    used_fn_indexes=[],
                    front_hand_count=4,
                    right_hand_count=4
                  )
                  ),
  PictureHelpCard("green", "## Choose functions to play", """\
# Each player chooses one or more function
# cards from their hand. When everybody
# selected their card(s), show them
# to others. For the first time, do not
# worry to select random ones.\
""",
                  lambda: get_play(
                    fns_count=8,
                    values_count=12,
                    input_value_index=3,
                    output_value_index=7,
                    used_fn_indexes=[],
                    front_hand_count=3,
                    right_hand_count=2,
                    front_played_count=1,
                    right_played_count=2,
                  )
                  ),
  PictureHelpCard("green", "## Compute result, example 1", """\
# Function card transforms input value
# into a different one. The goal is to get
# as close to output value as possible.\
""",
                  lambda: get_first_chain_image()
                  ),
  PictureHelpCard("green", "## Compute result, example 2", """\
# More functions can be combined
# for better result. See Function guide
# to learn how to use them.\
""",
                  lambda: get_second_chain_image()
                  ),
  PictureHelpCard("green", "## Put away used functions", """\
# Used functions are put away, if there's
# not enough of unused functions, mix
# the used ones and add them to the bottom
# of the unused ones\
""",
                  lambda: get_play(
                    fns_count=8,
                    values_count=12,
                    input_value_index=3,
                    output_value_index=7,
                    used_fn_indexes=[5, 2, 7],
                    front_hand_count=3,
                    right_hand_count=2,
                  )
                  ),
  PictureHelpCard("green", "## Get new function cards", """\
# Each player gets as many new cards
# as he used, only winners,
# those who were closest to output value,
# get one card less\
""",
                  lambda: get_play(
                    fns_count=6,
                    values_count=12,
                    input_value_index=3,
                    output_value_index=7,
                    used_fn_indexes=[5, 2, 7],
                    front_hand_count=4,
                    right_hand_count=3,
                  )
                  ),
  PictureHelpCard("green", "## Game end", """\
# Play the round as long as somebody has
# no cards, that player wins the game.
# When you manage green cards, you can
# add yellow ones, then red and finally
# white ones.\
""",
                  lambda: get_play(
                    fns_count=6,
                    values_count=6,
                    input_value_index=8,
                    output_value_index=7,
                    used_fn_indexes=[5, 2, 7, 4, 8, 9, 11, 6],
                    front_hand_count=2,
                    right_hand_count=0,
                  )
                  )
]
