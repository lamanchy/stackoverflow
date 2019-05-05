# -*- coding: utf-8 -*-
import inspect
import os
import random
import re
from math import ceil
from random import randint

import numpy
from PIL import Image, ImageFont, ImageDraw, ImageColor

from help_cards import get_all_help_cards
from rules import get_rules, get_all_functions
from values import get_all_values, values

FONT = "fonts/DejaVuSansMono.ttf"
FONT_BOLD = "fonts/DejaVuSansMono-Bold.ttf"


HIGH_QUALITY = True
if HIGH_QUALITY:
  RESAMPLE_WAY = Image.BICUBIC
  RESIZE_WAY = Image.ANTIALIAS
  RESOLUTION_DPI = 300
  ANTIALIASING = 3

else:
  RESAMPLE_WAY = Image.NEAREST
  RESIZE_WAY = Image.NEAREST
  RESOLUTION_DPI = 115
  ANTIALIASING = 1

TEXTURE = "textures/moulin.png"
TEXTURE = "textures/slash_it.png"
TEXTURE = "textures/what-the-hex-dark.png"
# TEXTURE = "textures/zig zag wool.png"
CARD_SIZE_MM = (87, 57)
# CARD_SIZE_MM = (93, 69)


def do_antialiasing(img):
  return img.resize((int(img.size[0] / ANTIALIASING), int(img.size[1] / ANTIALIASING)), RESIZE_WAY)


def show(img):
  do_antialiasing(img).show()

# dasda


def mm_to_px(*args):
  x = args
  if len(args) == 1:
    x = args[0]
  if isinstance(x, int) or isinstance(x, float):
    return int(RESOLUTION_DPI * ANTIALIASING * 0.03937 * x)

  return type(x)([mm_to_px(i) for i in x])


def get_font(size, font=FONT):
  return ImageFont.truetype(font, size=int(size * RESOLUTION_DPI * ANTIALIASING / 100))


color_codes = {
  "black": "#2b2b2b",
  "true_black": "#000000",
  "lighter_black": "#313335",
  "white": "rgb(212,225,240)",
  "true_white": "#FFFFFF",
  "blue": "rgb(102,180,250)",
  "violet": "rgb(169,168,255)",
  "orange": "rgb(230,142,71)",
  "yellow": "#FFC66D",
  "green": "rgb(100,183,70)",
  "grey": "rgb(166,166,166)",
  "red": "rgb(216,69,65)",
  "cyan": "rgb(82,187,186)",
  "magenta": "rgb(194,158,211)",
}

img_box_move = 20.0
box_size = (CARD_SIZE_MM[0] - img_box_move, CARD_SIZE_MM[0] - img_box_move)

random.seed(10)
def get_base(base_color):
  size = (CARD_SIZE_MM[0], CARD_SIZE_MM[1] * 2)
  color = ImageColor.getrgb(color_codes["true_black"])
  base = Image.new('RGBA', mm_to_px(size), (*color, 255))
  color = ImageColor.getrgb(color_codes["lighter_black"])
  base.paste(
    Image.new('RGB', mm_to_px((size[0] - 6, size[1] - 6)), color),
    mm_to_px(3, 3)
  )
  color = blendify_color(base_color)
  base.paste(
    Image.new('RGB', mm_to_px((size[0] - 7, size[1] - 7)), color),
    mm_to_px(3.5, 3.5)
  )
  color = ImageColor.getrgb(color_codes["black"])
  base.paste(
    Image.new('RGB', mm_to_px((size[0] - 8, size[1] - 8)), color),
    mm_to_px(4, 4)
  )

  return base


def find_coefficients(pa, pb):
  matrix = []
  for p1, p2 in zip(pa, pb):
    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

  A = numpy.matrix(matrix, dtype=numpy.float)
  B = numpy.array(pb).reshape(8)

  res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
  return numpy.array(res).reshape(8)


def get_base_with_box(base_color):
  base = get_base(base_color)
  color = ImageColor.getrgb(color_codes["grey"])
  base.paste(
    Image.new('RGB', mm_to_px((CARD_SIZE_MM[0] - (img_box_move - 0.5), CARD_SIZE_MM[0] - (img_box_move - 0.5))), color),
    mm_to_px((img_box_move - 0.5) / 2, (img_box_move - 0.5) / 2)
  )
  color = ImageColor.getrgb(color_codes["black"])
  base.paste(
    Image.new('RGB', mm_to_px(box_size), color),
    mm_to_px(img_box_move / 2, img_box_move / 2)
  )

  return base


def get_picture_card(heading, text, picture, top=False):
  if picture is not None:
    t = get_base_with_box("cyan")
  else:
    t = get_base("cyan")

  draw = ImageDraw.Draw(t)
  font = get_font(15)
  x = img_box_move / 2 + 2
  y = CARD_SIZE_MM[0] - x / 2
  if top: y = x
  draw.text(mm_to_px(x, y), text=heading, fill=color_codes["white"], font=font,
            spacing=mm_to_px(0.8))
  font = get_font(11)
  y += 7
  draw.text(mm_to_px(x, y), text=text, fill=color_codes["white"], font=font,
            spacing=mm_to_px(0.8))

  if picture is not None:
    t.paste(
      picture.crop((0, 0, mm_to_px(CARD_SIZE_MM[0] - img_box_move)
                    , mm_to_px(CARD_SIZE_MM[0] - img_box_move))),
      mm_to_px(img_box_move / 2, img_box_move / 2)
    )

  return t


def get_main_plane_coeffs(plane_size, ratio, height):
  card_height = mm_to_px(0.36 * height)
  shrink_x = (plane_size[0] - (plane_size[0] * ratio)) / 2
  return find_coefficients(
    [
      (shrink_x, - card_height * ratio),
      (plane_size[0] - shrink_x, - card_height * ratio),
      (plane_size[0], plane_size[1] * ratio - card_height),
      (0, plane_size[1] * ratio - card_height)
    ],
    [(0, 0), (plane_size[0], 0), (plane_size[0], plane_size[1]), (0, plane_size[1])]
  )


def get_first_image():
  background = ImageColor.getrgb(color_codes["lighter_black"])

  fn = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  fn_back = get_card_back("yellow").rotate(90, expand=True, resample=RESAMPLE_WAY)
  fn.paste(fn_back, mm_to_px(00, 45), fn_back)

  value = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  value_back = get_card_back("blue").rotate(90, expand=True, resample=RESAMPLE_WAY)
  value.paste(value_back, mm_to_px(70, 45), value_back)

  corner_size = 20
  cropped_fn = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  cropped_fn_back = get_card_back("yellow").rotate(90, expand=True, resample=RESAMPLE_WAY)
  for w in range(cropped_fn_back.width):
    for h in range(cropped_fn_back.height):
      if w - h > mm_to_px(CARD_SIZE_MM[1] - corner_size):
        cropped_fn_back.putpixel((w, h), (0, 0, 0, 0))

  cropped_fn.paste(cropped_fn_back, mm_to_px(00, 45), cropped_fn_back)

  cropped_fn_corner = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  cropped_fn_corner_back = get_card_back("green").rotate(90, expand=True, resample=RESAMPLE_WAY)
  for w in range(cropped_fn_corner_back.width):
    for h in range(cropped_fn_corner_back.height):
      if w - h <= mm_to_px(CARD_SIZE_MM[1] - corner_size - 0.1):
        cropped_fn_corner_back.putpixel((w, h), (0, 0, 0, 0))
        continue
      if w - h <= mm_to_px(CARD_SIZE_MM[1] - corner_size):
        pix = list(cropped_fn_corner_back.getpixel((w, h)))
        for i in range(len(pix)):
          pix[i] //= 2
        pix[-1] = 255
        cropped_fn_corner_back.putpixel((w, h), tuple(pix))

  cropped_fn_corner_back = cropped_fn_corner_back.rotate(
    180, center=mm_to_px(CARD_SIZE_MM[1] - corner_size // 2, corner_size // 2), resample=RESAMPLE_WAY)
  cropped_fn_corner.paste(cropped_fn_corner_back, mm_to_px(00, 45), cropped_fn_corner_back)

  plane = Image.new("RGBA", mm_to_px(200, 150), (*background, 255))
  blank = Image.new("RGBA", mm_to_px(200, 150), (*background, 255))
  for height in range(16):
    ratio = .8
    coeffs = get_main_plane_coeffs(plane.size, ratio, height - 0.5)
    transformed = value.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
    plane.paste(blank, mask=transformed)

    if height < 13:
      transformed = fn.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      plane.paste(blank, mask=transformed)
    if height == 13:
      transformed = cropped_fn.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      plane.paste(blank, mask=transformed)
    if height == 14:
      transformed = cropped_fn_corner.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      plane.paste(blank, mask=transformed)

    coeffs = get_main_plane_coeffs(plane.size, ratio, height)
    transformed = value.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
    plane.paste(transformed, mask=transformed)
    if height <= 14:
      if height < 13:
        transformed = fn.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      if height == 13:
        transformed = cropped_fn.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      if height == 14:
        transformed = cropped_fn_corner.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
      plane.paste(transformed, mask=transformed)

  plane = plane.resize((plane.width // 2, plane.height // 2), RESIZE_WAY)

  return plane


def get_chain_image(cards, x, y, scale):
  background = ImageColor.getrgb(color_codes["lighter_black"])
  plane = Image.new("RGBA", mm_to_px(200, 200), (*background, 255))

  for i in range(len(cards)):
    card = Image.new("RGBA", mm_to_px(200, 200), (*background, 0))
    to_paste = cards[i]
    card.paste(to_paste, mm_to_px(i * 20 + x, y + i * 40), to_paste)

    coeffs = get_main_plane_coeffs(plane.size, .9, i)
    transformed = card.transform(plane.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
    plane.paste(transformed, mask=transformed)

  return plane.resize((int(plane.width / scale), int(plane.height / scale)), RESIZE_WAY)


def get_first_chain_image():
  return get_chain_image(
    [
      get_value_card_front(0, values["green"][3], "green"),
      get_fn_card_front(0, get_rules()["green"][5], "green"),
      get_value_card_front(0, values["green"][7], "green")
    ], 7, 5, 2.2
  )


def get_second_chain_image():
  return get_chain_image(
    [
      get_value_card_front(0, values["green"][3], "green"),
      get_fn_card_front(0, get_rules()["green"][2], "green"),
      get_fn_card_front(0, get_rules()["green"][7], "green"),
      get_value_card_front(0, values["green"][7], "green"),
    ], 11, 5, 2.5
  )


def get_play_board():
  return Image.new("RGBA", mm_to_px(400, 400), (0, 0, 0, 0))


def transform_play_board(board, height):
  scale = 5
  if not HIGH_QUALITY:
    board = board.resize((int(board.width / scale), int(board.height / scale)), RESIZE_WAY)
    height /= 5

  coeffs = get_main_plane_coeffs(board.size, .5, height)
  res = get_play_board()

  board = board.rotate(80, expand=True, resample=RESAMPLE_WAY)
  board = board.transform(board.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)

  if HIGH_QUALITY:
    board = board.resize((int(board.width / scale), int(board.height / scale)), RESIZE_WAY)

  res.paste(board, mm_to_px(-15, 10), mask=board)
  return res


def get_play(
    fns_count, values_count,
    input_value_index, output_value_index,
    used_fn_indexes,
    front_hand_count, right_hand_count,
    front_played_count=0, right_played_count=0
):
  background = ImageColor.getrgb(color_codes["lighter_black"])
  base = Image.new("RGBA", mm_to_px(box_size), (*background, 255))

  x1 = 30
  x2 = 230
  y1 = 30
  y2 = 100

  table = get_play_board()
  table.putalpha(100)
  table = transform_play_board(table, 0)
  base.paste(table, mask=table)

  blank = get_play_board()

  fn = get_play_board()
  fn_card = get_card_back("yellow")
  fn.paste(fn_card, mm_to_px(x2, y1), fn_card)

  for i in range(fns_count):
    transformed = transform_play_board(fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(fn, i)
    base.paste(transformed, mask=transformed)

  value = get_play_board()
  value_card = get_card_back("blue")
  value.paste(value_card, mm_to_px(x1, y1), value_card)

  for i in range(values_count):
    transformed = transform_play_board(value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(value, i)
    base.paste(transformed, mask=transformed)

  used_value = get_play_board()
  used_value_card = get_value_card_front(0, values["green"][0], "green")
  used_value.paste(used_value_card, mm_to_px(x1, y2), used_value_card)

  for i in range(14 - values_count - 1):
    transformed = transform_play_board(used_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(used_value, i)
    base.paste(transformed, mask=transformed)

  if input_value_index is not None:
    input_value = get_play_board()
    input_value_card = get_value_card_front(0, values["green"][input_value_index], "green")
    input_value.paste(input_value_card, mm_to_px(x1, y2), input_value_card)

    i = 14 - values_count - 1
    transformed = transform_play_board(input_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(input_value, i)
    base.paste(transformed, mask=transformed)

  if output_value_index is not None:
    output_value = get_play_board()
    output_value_card = get_value_card_front(0, values["green"][output_value_index], "green")
    output_value.paste(output_value_card, mm_to_px(x2, y2), output_value_card)

    i = 0
    transformed = transform_play_board(output_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(output_value, i)
    base.paste(transformed, mask=transformed)

  for i in range(right_hand_count):
    right_hand = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    right_hand_tmp = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    right_hand_card = get_card_back("yellow")
    right_hand_tmp.paste(right_hand_card, mm_to_px(50, 50), right_hand_card)
    # right_hand_tmp = right_hand_tmp.resize((2 * right_hand_tmp.size[0], 2 * right_hand_tmp.size[1]))
    right_hand_tmp = right_hand_tmp.rotate(13 + (-i - 1) * 8, center=mm_to_px((CARD_SIZE_MM[0] + 50, 50)),
                                           resample=RESAMPLE_WAY)
    right_hand.paste(right_hand_tmp, mm_to_px(0, 80), right_hand_tmp)
    right_hand = right_hand.rotate(180, resample=RESAMPLE_WAY)

    coeffs = find_coefficients(
      [
        (mm_to_px(140), mm_to_px(20)),
        (right_hand.size[0] - mm_to_px(20), mm_to_px(40)),
        (right_hand.size[0] - mm_to_px(20), right_hand.size[1] - mm_to_px(130)),
        (mm_to_px(160), right_hand.size[1] - mm_to_px(140))
      ],
      [(0, 0), (right_hand.size[0], 0), (right_hand.size[0], right_hand.size[1]), (0, right_hand.size[1])]
    )
    right_hand = right_hand.transform(right_hand.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
    scale = 1.5
    right_hand = right_hand.resize((int(right_hand.width / scale), int(right_hand.height / scale)), RESIZE_WAY)
    base.paste(right_hand, mm_to_px(-110 / scale + 23, -30 / scale + 2), mask=right_hand)

  for i in range(len(used_fn_indexes)):
    used_fn = get_play_board()
    used_fn_card = get_fn_card_front(0, get_rules()["green"][used_fn_indexes[i]], "green")
    used_fn_card = used_fn_card.rotate(randint(0, 360), resample=RESAMPLE_WAY, expand=True)

    used_fn.paste(used_fn_card, mm_to_px(x1 / 2 + x2 / 2 - 5, y2 + 30), used_fn_card)

    transformed = transform_play_board(used_fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(used_fn, i)
    base.paste(transformed, mask=transformed)

  for i in range(front_played_count):
    i += 1
    front_player_fn = get_play_board()
    front_player_fn_card = get_card_back("yellow")
    front_player_fn_card = front_player_fn_card.rotate(97 + 10 * -i, expand=True, resample=RESAMPLE_WAY)
    front_player_fn.paste(front_player_fn_card,
                          mm_to_px(x1 - 10 + 2 * i + randint(-3, 3), 200 + 20 * i + randint(-3, 3)),
                          front_player_fn_card)

    transformed = transform_play_board(front_player_fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(front_player_fn, i)
    base.paste(transformed, mask=transformed)

  for i in range(right_played_count):
    i += 1
    right_player_fn = get_play_board()
    right_player_fn_card = get_card_back("yellow")
    right_player_fn_card = right_player_fn_card.rotate(51 + 8 * -i, expand=True, resample=RESAMPLE_WAY)
    right_player_fn.paste(right_player_fn_card,
                          mm_to_px(x2 + 20 + 8 * i + randint(-3, 3), 300 - 20 * i + randint(-3, 3)),
                          right_player_fn_card)

    transformed = transform_play_board(right_player_fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(right_player_fn, i)
    base.paste(transformed, mask=transformed)

  for i in range(front_hand_count):
    front_hand = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    front_hand_tmp = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    front_hand_card = get_value_card_front(0, values["green"][0], "green")
    front_hand_tmp.paste(front_hand_card, mm_to_px(50, 50), front_hand_card)
    # front_hand_tmp = front_hand_tmp.resize((2 * front_hand_tmp.size[0], 2 * front_hand_tmp.size[1]))
    front_hand_tmp = front_hand_tmp.rotate(-2 + (-i - 1) * 5,
                                           center=mm_to_px((CARD_SIZE_MM[0] + 50, CARD_SIZE_MM[1] + 50)),
                                           resample=RESAMPLE_WAY)
    front_hand.paste(front_hand_tmp, mm_to_px(0, 0), front_hand_tmp)

    coeffs = get_main_plane_coeffs(front_hand.size, .9, i)
    front_hand = front_hand.transform(front_hand.size, Image.PERSPECTIVE, coeffs, resample=RESAMPLE_WAY)
    scale = 2
    front_hand = front_hand.resize((int(front_hand.width / scale), int(front_hand.height / scale)), RESIZE_WAY)
    base.paste(front_hand, mm_to_px(-12, 46), mask=front_hand)

  return base


def get_first_play():
  return get_play(
    fns_count=8,
    values_count=13,
    input_value_index=None,
    output_value_index=7,
    used_fn_indexes=[],
    front_hand_count=4,
    right_hand_count=4
  )




# noinspection SqlNoDataSourceInspection
def get_picture_cards(i):
  if i == 0:
    return (
      "Hello to Stack Overflow",
      """\
If you wanna jump to playing the game,
don't worry, go ahead. But if you are not
in hurry, there are few lines for you:

This game is hard. Well, not difficult,
at least not at the easiest difficulty,
even my 11 years old sister-in-law can
play it. But I'll warn you, you'll have
to use your head. A lot.

Furthermore, even learning this game can
be a bit of challenge in itself, maybe
not so much for a skilled programmer, but
if you've forgotten, what prime is, you
will learn a thing or two. Programming,
for example. Well, not all of it, but..
the important stuff, I would say.

And at the end, there's feeling like no
other, not when you win by a luck, but
by your knowledge and skill. When victory
is deserved, it tastes much sweeter.

I hope you'll have fun.
                                      B.\
""",
      None,
      True
    )
  if i == 1:
    return (
      "Firstly select the difficulty",
      """\
Find all cards with green face (that's
the easiest difficulty), then split
the cards by back color, values are blue
and functions are orange.\
""",
      get_first_image()
    )
  if i == 2:
    return (
      "At the beginning of each game",
      """\
Select output value, from value deck.
Each player gets 4 functions.

Game is prepared, now play rounds
as long as nobody wins.\
""",
      get_play(
        fns_count=8,
        values_count=13,
        input_value_index=None,
        output_value_index=7,
        used_fn_indexes=[],
        front_hand_count=4,
        right_hand_count=4
      )
    )
  if i == 3:
    return (
      "Select new input value",
      """\
There is a new input value each round,
output value stays the same
for a whole game\
""",
      get_play(
        fns_count=8,
        values_count=12,
        input_value_index=3,
        output_value_index=7,
        used_fn_indexes=[],
        front_hand_count=4,
        right_hand_count=4
      )
    )
  if i == 4:
    return (
      "Choose functions to play",
      """\
Each player chooses one or more function
cards from their hand. When everybody
selected their card(s), show them
to others. For the first time, do not
worry to select random ones.\
""",
      get_play(
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
    )
  if i == 5:
    return (
      "Compute result, example 1",
      """\
Function card transforms input value
into a different one. The goal is to get
as close to output value as possible.\
""",
      get_first_chain_image()
    )
  if i == 6:
    return (
      "Compute result, example 2",
      """\
More functions can be combined for better
result. See Function guide to learn
how to use them.\
""",
      get_second_chain_image()
    )
  if i == 7:
    return (
      "Compute result, example 2",
      """\
Used functions are put away, if there's
not enough of unused functions, mix
the used ones and add them to the bottom
of the unused ones\
""",
      get_play(
        fns_count=8,
        values_count=12,
        input_value_index=3,
        output_value_index=7,
        used_fn_indexes=[5, 2, 7],
        front_hand_count=3,
        right_hand_count=2,
      )
    )
  if i == 8:
    return (
      "Get new function cards",
      """\
Each player gets as many new cards
as he used, only winners,
those who were closest to output value,
get one card less\
""",
      get_play(
        fns_count=6,
        values_count=12,
        input_value_index=3,
        output_value_index=7,
        used_fn_indexes=[5, 2, 7],
        front_hand_count=4,
        right_hand_count=3,
      )
    )
  if i == 9:
    return (
      "Game end",
      """\
Play the round as long as somebody has
no cards, that player wins the game.
Good luck\
""",
      get_play(
        fns_count=6,
        values_count=6,
        input_value_index=8,
        output_value_index=7,
        used_fn_indexes=[5, 2, 7, 4, 8, 9, 11, 6],
        front_hand_count=2,
        right_hand_count=0,
      )
    )



def get_source_code(fn):
  source_code = inspect.getsource(fn)

  # remove leading and ending spaces
  source_code = source_code.strip().split('\n')

  for i in range(len(source_code)-1, -1, -1):
    if "# DEBUG this line wont be printed" in source_code[i]:
      source_code = source_code[:i] + source_code[i+1:]

    if source_code[i].startswith('@'):
      source_code = source_code[:i] + source_code[i + 1:]

  source_code = '\n'.join(source_code)

  if source_code.startswith("lambda") and source_code[-1] == ',':
    source_code = source_code[:-1]

  return source_code


def get_source_code_name(source_code):
  if not isinstance(source_code, str):
    source_code = get_source_code(source_code)

  source_code = source_code.split('\n')[0]
  colloring = get_source_code_coloring(source_code)

  if source_code.startswith("def"):
    start = len("def ")
    end = len(source_code) - 1
    while source_code[end] != '(':
      end -= 1

  else:
    start = len("lambda x: ")
    end = len(source_code)

  source_code = source_code[start:end]
  for color in colloring:
    colloring[color] = colloring[color][start:end]

  return source_code, colloring


card_colors_to_real_colors = {
  "green": "green",
  "yellow": "yellow",
  "red": "red",
  "black": "white",
  "magenta": "magenta",
  "cyan": "cyan",
}

color_regexes = [
  (r".*", "white"),  # default color
  (r"(?:\W|^)(\d+)", "blue"),
  (r"(-|\.)(?=\d)", "blue"),
  (r"(√|π|pi|inf)", "blue"),
  (
    r'(?:^|\s|\(|\[)(round|range|abs|max|min|floor|len|gcd|lcm|is_prime|sqrt|ceil|log2|sin|int|str'
    r'|pow|float|eval|sign|isnan|input|get_all_cards|shuffle|all|enumerate'
    r'|isinf|ZeroDivisionError|ValueError|TypeError|RecursionError|Exception)(?=\(|:|\s|\)|,|$)',
    "violet"),
  (r'(?:^|\s|=)(lambda|def|if|while|and|or|else|elif|for|in|return|None|global'
   r'|is|except|try|as)(?=\W|:|\))', "orange"),
  (r'def (\w*)', "yellow"),
  (r"'[^'\n]*'", "green"),
  (r'"[^"]*"', "green"),
  (r'#\s.*', "grey"),
  (r'ě', "green"),
  (r'š', "yellow"),
  (r'č', "red"),
  (r'ř', card_colors_to_real_colors["black"]),
]


def get_source_code_coloring(string):
  colors = [color_regexes[0][1] for i in range(len(string))]
  for regex, color in color_regexes:
    for match in re.finditer(regex, string):
      if len(match.groups()) > 0:
        span = match.span(1)
      else:
        span = match.span()

      for i in range(*span):
        colors[i] = color

  result = {}

  for color in set(colors):
    result[color] = ""
    for char, char_color in zip(string, colors):
      if char in "ěščř": char = "⧫" # ●∙
      if not re.match(r'\s', char) and char_color != color:
        char = " "
      result[color] += char

  return result


def apply_texture(image, texture):
  texture = Image.open(texture)
  texture = texture.resize((texture.size[0] * ANTIALIASING, texture.size[1] * ANTIALIASING), resample=RESIZE_WAY)
  texture = texture.point(lambda p: p * 2)
  for x in range(0, image.size[0], texture.size[0]):
    for y in range(0, image.size[1], texture.size[1]):
      image.paste(texture, (x, y), mask=image.crop((x, y, x + texture.size[0], y + texture.size[1])))


def get_round_rectangle(size=CARD_SIZE_MM, color="black", radius=10.0, texture=None):
  if isinstance(color, str): color = ImageColor.getrgb(color_codes[color])
  if not isinstance(color, tuple): color = tuple(color)
  rectangle = Image.new('RGBA', mm_to_px(size), (*color, 0))
  draw = ImageDraw.Draw(rectangle)
  draw.rectangle(mm_to_px(radius / 2, 0, size[0] - (radius / 2), size[1]), fill=color)
  draw.rectangle(mm_to_px(0, radius / 2, size[0], size[1] - (radius / 2)), fill=color)
  draw.ellipse(mm_to_px(0, 0, radius, radius), fill=color)
  draw.ellipse(mm_to_px(size[0] - radius, 0, size[0], radius), fill=color)
  draw.ellipse(mm_to_px(0, size[1] - radius, radius, size[1]), fill=color)
  draw.ellipse(mm_to_px(size[0] - radius, size[1] - radius, size[0], size[1]), fill=color)
  if texture is not None:
    apply_texture(rectangle, texture)

  return rectangle


def get_card_base(multipler=(1, 1), round=True):
  radius = 0
  if round: radius = 10
  size = (CARD_SIZE_MM[0]*multipler[0], CARD_SIZE_MM[1]*multipler[1])
  card = get_round_rectangle(size, "true_black", radius=radius)
  if round: radius = 6
  border = get_round_rectangle((size[0] - 6, size[1] - 6), "lighter_black", radius=radius)
  card.paste(border, mm_to_px(3, 3), mask=border)
  if round: radius = 4
  background = get_round_rectangle((size[0] - 8, size[1] - 8), "black", radius=radius)
  card.paste(background, mm_to_px(4, 4), mask=background)
  return card


def get_order_sign_n_color(order):
  sign = "♠"
  if order % 4 == 1: sign = u"♣"
  if order % 4 == 2: sign = u"♥"
  if order % 4 == 3: sign = u"♦"

  number = (8 + order) // 4
  if number == 11:
    number = "J"
  elif number == 12:
    number = "Q"
  elif number == 13:
    number = "K"
  elif number == 14:
    number = "A"
  else:
    number = str(number)
  return sign + number, "orange" if (order // 2) % 2 == 1 else "blue"


def blendify_color(color):
  color = list(ImageColor.getrgb(color_codes[card_colors_to_real_colors[color]]))
  for i in range(len(color)): color[i] //= 1.5
  for i in range(len(color)): color[i] = int(color[i])
  return tuple(color)


def get_card_base_with_color(order, color, multipler=(1, 1), round=True):
  card = get_card_base(multipler, round)
  smaller_by = 0
  border_color = blendify_color(color)

  radius = 0
  if round: radius = 5-smaller_by
  border = get_round_rectangle((CARD_SIZE_MM[0]*multipler[0] - 7 - smaller_by, CARD_SIZE_MM[1]*multipler[1] - 7 - smaller_by), border_color, radius=radius)
  card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 6, CARD_SIZE_MM[1] - 6), "lighter_black", radius=6)
  # card.paste(border, mm_to_px(4, 3), mask=border)
  if round: radius = 4
  background = get_round_rectangle((CARD_SIZE_MM[0]*multipler[0] - 8, CARD_SIZE_MM[1]*multipler[1] - 8), "black", radius=radius)
  card.paste(background, mm_to_px(4, 4), mask=background)
  # background = get_round_rectangle((CARD_SIZE_MM[0] - 9, CARD_SIZE_MM[1] - 9), "black", radius=3)
  # card.paste(background, mm_to_px(4.5, 4.5), mask=background)
  # draw = ImageDraw.Draw(card)
  # base_size = 10
  # move_up = 3.5
  # move_left = 3.5
  # smaller_by = -.5
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes["lighter_black"])
  # smaller_by = .5
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes[card_colors_to_real_colors[color]])
  # smaller_by = 1
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes["true_black"])

  # font = get_font(15, FONT_BOLD)
  # sign, color = get_order_sign_n_color(order)
  # w, _ = draw.textsize(sign, font)
  # _, h = draw.textsize("8", font)
  # draw.text(
  #   (
  #     mm_to_px(move_left + base_size // 2) - w // 2 - mm_to_px(.1),
  #     mm_to_px(CARD_SIZE_MM[1] - base_size // 2 - move_up) - h // 2 - mm_to_px(.45)
  #   ),
  #   sign, font=font, fill=color_codes[color])

  return card


def get_source_code_position_n_size(card, source_code, draw):
  # width is exactly half the height

  min_font_size = 1
  max_font_size = 25
  height_multipler = card.size[1] // mm_to_px(CARD_SIZE_MM[1])
  available_size = list((card.size[0] - mm_to_px(10), card.size[1] - mm_to_px(5*(height_multipler-1) + 30)))

  while True:
    size = draw.textsize(source_code, get_font(min_font_size + 1), spacing=mm_to_px(.13))

    if size[0] >= available_size[0] or size[1] >= available_size[1] or min_font_size == max_font_size:
      if (height_multipler == 1 and min_font_size < 15) or (height_multipler == 2 and min_font_size < 11):
        print("too small font size, fn {}, font size {}".format(source_code.split('\n')[0], min_font_size))
        print(size, available_size)
      return min_font_size

    min_font_size += 1
    available_size[0] *= .99


def get_fn_card_front(order, fn, color):
  source_code = get_source_code(fn)
  colors = get_source_code_coloring(source_code)

  card = get_card_base_with_color(order, color)
  base = Image.new("RGBA", mm_to_px(CARD_SIZE_MM), (0, 0, 0, 0))
  draw = ImageDraw.Draw(base)
  sc_size = get_source_code_position_n_size(card, source_code, draw)
  font = get_font(sc_size)
  W, H = mm_to_px(CARD_SIZE_MM)
  w, h = draw.textsize(source_code, font)

  for color in colors:
    draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(1)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))

  # name, name_colloring = get_source_code_name(fn)
  # font = get_font(10)
  # w, h = draw.textsize(name, font)
  #
  # for color in name_colloring:
  #   draw.text((mm_to_px(15), H - h - mm_to_px(5)), name_colloring[color], font=font, fill=color_codes[color])

  card.paste(base, mask=base)

  return card


def get_value_card_front(order, value, color):
  value = value[1]
  card = get_card_base_with_color(order, color)
  draw = ImageDraw.Draw(card)
  font = get_font(50)
  W, H = mm_to_px(CARD_SIZE_MM)
  w, h = draw.textsize(value, font)
  if value[0] in '-':
    w += draw.textsize('-', font)[0]

  # draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(3)), value, font=font, fill=color_codes["blue"])
  colors = get_source_code_coloring(value)
  for color in colors:
    draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))
  # draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), value, font=font, fill=color_codes["blue"])

  return card


def get_card_back(color):
  # card = get_card_base()
  # for i, text in enumerate(["Stack\n", "Overflow\n"]):
  #   invisible = Image.new('RGBA', mm_to_px(CARD_SIZE_MM), (0, 0, 0, 0))
  #   draw = ImageDraw.Draw(invisible)
  #   W, H = mm_to_px(CARD_SIZE_MM)
  #   # font = get_font(17)
  #   font = get_font(25)
  #   w, h = draw.textsize(text, font)
  #   draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), text, font=font, fill=color_codes[color])
  #
  #   invisible = invisible.rotate(i*180)
  #   card.paste(invisible, mask=invisible)

  card = get_card_base()

  smaller_by = -2
  border_color = list(ImageColor.getrgb(color_codes[color]))
  for i in range(len(border_color)): border_color[i] /= 1.2
  for i in range(len(border_color)): border_color[i] = int(max(border_color[i] - 100, 0))
  # smaller_by = -7
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), border_color, radius=5-smaller_by)
  # card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # smaller_by = -6
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "true_black", radius=5-smaller_by)
  # card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 6, CARD_SIZE_MM[1] - 6), "lighter_black", radius=6)
  # card.paste(border, mm_to_px(4, 3), mask=border)
  smaller_by = -1
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), border_color,
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)
  smaller_by = 0
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "lighter_black",
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)
  smaller_by = 1
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "black",
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)

  draw = ImageDraw.Draw(card)
  text = "Stack Overflow"
  W, H = mm_to_px(CARD_SIZE_MM)
  font = get_font(20)
  w, h = draw.textsize(text, font)
  draw.text(((W - w) // 2, (H - h) // 2), text, font=font, fill=color_codes[color])
  return card.rotate(180)


def get_fn_card(order, fn, color):
  return get_fn_card_front(order, fn, color), get_card_back("yellow")


def get_help_card(help_text):
  title, source_code = help_text.split('\n', 1)
  # print(source_code)
  color = "cyan" if "PLAY THIS GAME" in title else "magenta"

  card = get_card_base_with_color(1, color, (1, 2), False)
  # card = get_card_base((1, 2))
  draw = ImageDraw.Draw(card)

  font = get_font(13)
  W, H = card.size
  w, h = draw.textsize(title, font)
  colors = get_source_code_coloring(title)
  for color in colors:
    draw.text((W - mm_to_px(6) - w, mm_to_px(5)), colors[color], font=font, fill=color_codes[color])

  sc_size = get_source_code_position_n_size(card, source_code, draw)
  font = get_font(sc_size)
  w, h = draw.textsize(source_code, font, spacing=mm_to_px(0.6))
  colors = get_source_code_coloring(source_code)

  for color in colors:
    draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(2)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))

  return card


def get_value_card(order, value, color):
  return get_value_card_front(order, value, color), get_card_back("blue")


if __name__ == "__main__":
  cards = []
  is_this_first_page = True

  try:
    os.remove("stack_overflow.pdf")
  except FileNotFoundError:
    pass


  def generate_pdf(last_time=False):
    if len(cards) < 10 and (not last_time or len(cards) == 0):
      return

    front_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
    back_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
    base_point = int(mm_to_px(210) / 2 - mm_to_px(CARD_SIZE_MM[0]) - mm_to_px(.05)), \
                 int(mm_to_px(297) / 2 - 2.5 * mm_to_px(CARD_SIZE_MM[1]) - mm_to_px(.2))

    for i, card in enumerate(cards[:10]):
      if card[0].size[0] == 0: continue
      offset_x = mm_to_px(CARD_SIZE_MM[0] + .1) if i % 2 == 1 else 0
      offset_y = mm_to_px(CARD_SIZE_MM[1] + .1) * (i // 2)

      front_canvas.paste(card[0], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[0])
      offset_x = mm_to_px(CARD_SIZE_MM[0] + .1) if i % 2 == 0 else 0
      background = get_round_rectangle((
        (card[1].size[0] // mm_to_px(CARD_SIZE_MM[0]))*CARD_SIZE_MM[0]+4,
        (card[1].size[1] // mm_to_px(CARD_SIZE_MM[1]))*CARD_SIZE_MM[1]+4), "true_black")
      back_canvas.paste(background, (base_point[0] + offset_x - mm_to_px(2), base_point[1] + offset_y - mm_to_px(2)), mask=background)
      back_canvas.paste(card[1], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[1])

    def save_canvas(canvas):
      canvas = do_antialiasing(canvas)
      try:
        canvas.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
                    resolution=RESOLUTION_DPI, append=True)
      except IOError:
        canvas.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
                    resolution=RESOLUTION_DPI, append=False)

    save_canvas(front_canvas)
    save_canvas(back_canvas)

    for i in range(min(len(cards), 10)):
      cards.pop(0)

  # for i, (fn, c) in enumerate(get_all_functions()):
  #   print(c, get_source_code(fn))


  def get_card():
    # for i, (fn, c) in enumerate(get_all_functions()[0:2] + get_all_functions()[16:18] + get_all_functions()[-8:-6] + get_all_functions()[-2:]):
    for i, (fn, c) in enumerate(get_all_functions()):
      yield get_fn_card(i, fn, c)

    # for i, (v, c) in enumerate(get_all_values()[0:2] + get_all_values()[16:18] + get_all_values()[-8:-6] + get_all_values()[-2:]):
    for i, (v, c) in enumerate(get_all_values()):
      yield get_value_card(i, v, c)

    while True:
      yield (Image.new("RGB", (0, 0)), Image.new("RGB", (0, 0)))

  card_generator = get_card()

  for page in range(int(ceil(len(get_all_help_cards())/4))):
    for i, (help1, help2) in enumerate(get_all_help_cards()[page*4:page*4+4]):
      if isinstance(help1, int):
        cards.append((get_picture_card(*get_picture_cards(help1)), get_picture_card(*get_picture_cards(help2))))
      else:
        cards.append((get_help_card(help1), get_help_card(help2)))
      if i in [1, 3]:
        for _ in range(2):
          cards.append((Image.new("RGB", (0, 0)), Image.new("RGB", (0, 0))))
        if i == 3:
          for _ in range(2):
            cards.append(card_generator.__next__())
      generate_pdf(False)

  while True:
    card = card_generator.__next__()
    if card[0].size[0] == 0: break
    cards.append(card)
    generate_pdf(False)

  generate_pdf(True)


  # i = Image.open("developing/napoveda_lic.jpg")
  # i.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
  #             resolution=300, append=True)
  # i = Image.open("developing/napoveda_rub.jpg")
  # i.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
  #        resolution=300, append=True)

