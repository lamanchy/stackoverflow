from random import randint

import numpy
from PIL import ImageColor, Image

from cards.card import Card
from cards.function_card import FunctionCard
from cards.picture_help_card import PictureHelpCard
from cards.playing_card_back import PlayingCardBack
from cards.value_card import ValueCard
from colors import color_codes
from pil_quality_pdf.rendering import mm_to_px
from pil_quality_pdf.transformation import rotate, transform, resize
from rules import get_rules
from values import values


def find_coefficients(pa, pb):
  matrix = []
  for p1, p2 in zip(pa, pb):
    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

  A = numpy.matrix(matrix, dtype=numpy.float)
  B = numpy.array(pb).reshape(8)

  res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
  return numpy.array(res).reshape(8)


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
  fn_back = rotate(PlayingCardBack("yellow").get_card(), 90)
  fn.paste(fn_back, mm_to_px(00, 45), fn_back)

  value = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  value_back = rotate(PlayingCardBack("blue").get_card(), 90)
  value.paste(value_back, mm_to_px(70, 45), value_back)

  corner_size = 20
  cropped_fn = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  cropped_fn_back = rotate(PlayingCardBack("yellow").get_card(), 90)
  for w in range(cropped_fn_back.width):
    for h in range(cropped_fn_back.height):
      if w - h > mm_to_px(Card.base_height - corner_size):
        cropped_fn_back.putpixel((w, h), (0, 0, 0, 0))

  cropped_fn.paste(cropped_fn_back, mm_to_px(00, 45), cropped_fn_back)

  cropped_fn_corner = Image.new("RGBA", mm_to_px(200, 150), (*background, 0))
  cropped_fn_corner_back = rotate(ValueCard("green", values["green"][0]).get_card(), 90)
  for w in range(cropped_fn_corner_back.width):
    for h in range(cropped_fn_corner_back.height):
      if w - h <= mm_to_px(Card.base_height - corner_size - 0.1):
        cropped_fn_corner_back.putpixel((w, h), (0, 0, 0, 0))
        continue
      if w - h <= mm_to_px(Card.base_height - corner_size):
        pix = list(cropped_fn_corner_back.getpixel((w, h)))
        for i in range(len(pix)):
          pix[i] //= 2
        pix[-1] = 255
        cropped_fn_corner_back.putpixel((w, h), tuple(pix))

  cropped_fn_corner_back = rotate(cropped_fn_corner_back, 180,
                                  expand=False, center=mm_to_px(Card.base_height - corner_size // 2, corner_size // 2))
  cropped_fn_corner.paste(cropped_fn_corner_back, mm_to_px(00, 45), cropped_fn_corner_back)

  plane = Image.new("RGB", mm_to_px(200, 150), (*background,))
  blank = Image.new("RGBA", mm_to_px(200, 150), (*background, 255))
  for height in range(16):
    ratio = .8
    coeffs = get_main_plane_coeffs(plane.size, ratio, height - 0.5)
    transformed = transform(value, plane.size, Image.PERSPECTIVE, coeffs)
    plane.paste(blank, mask=transformed)

    if height < 13:
      transformed = transform(fn, plane.size, Image.PERSPECTIVE, coeffs)
      plane.paste(blank, mask=transformed)
    if height == 13:
      transformed = transform(cropped_fn, plane.size, Image.PERSPECTIVE, coeffs)
      plane.paste(blank, mask=transformed)
    if height == 14:
      transformed = transform(cropped_fn_corner, plane.size, Image.PERSPECTIVE, coeffs)
      plane.paste(blank, mask=transformed)

    coeffs = get_main_plane_coeffs(plane.size, ratio, height)
    transformed = transform(value, plane.size, Image.PERSPECTIVE, coeffs)
    plane.paste(transformed, mask=transformed)
    if height <= 14:
      if height < 13:
        transformed = transform(fn, plane.size, Image.PERSPECTIVE, coeffs)
      if height == 13:
        transformed = transform(cropped_fn, plane.size, Image.PERSPECTIVE, coeffs)
      if height == 14:
        transformed = transform(cropped_fn_corner, plane.size, Image.PERSPECTIVE, coeffs)
      plane.paste(transformed, mask=transformed)

  plane = resize(plane, (plane.width // 2, plane.height // 2))

  return plane


def get_chain_image(cards, x, y, scale):
  background = ImageColor.getrgb(color_codes["lighter_black"])
  plane = Image.new("RGB", mm_to_px(200, 200), (*background,))

  for i in range(len(cards)):
    card = Image.new("RGBA", mm_to_px(200, 200), (*background, 0))
    to_paste = cards[i]
    card.paste(to_paste, mm_to_px(i * 20 + x, y + i * 40), to_paste)

    coeffs = get_main_plane_coeffs(plane.size, .9, i)
    transformed = transform(card, plane.size, Image.PERSPECTIVE, coeffs)
    plane.paste(transformed, mask=transformed)

  return resize(plane, (int(plane.width / scale), int(plane.height / scale)))


def get_first_chain_image():
  return get_chain_image(
    [
      ValueCard("green", values["green"][3]).get_card(),
      FunctionCard("green", get_rules()["green"][5]).get_card(),
      ValueCard("green", values["green"][7]).get_card()
    ], 7, 5, 2.2
  )


def get_second_chain_image():
  return get_chain_image(
    [
      ValueCard("green", values["green"][3]).get_card(),
      FunctionCard("green", get_rules()["green"][2]).get_card(),
      FunctionCard("green", get_rules()["green"][7]).get_card(),
      ValueCard("green", values["green"][7]).get_card(),
    ], 11, 5, 2.5
  )


def get_play_board():
  return Image.new("RGBA", mm_to_px(400, 400), (0, 0, 0, 0))


def transform_play_board(board, height):
  scale = 5
  board = resize(board, (int(board.width / scale), int(board.height / scale)))
  height /= 5

  coeffs = get_main_plane_coeffs(board.size, .5, height)
  res = get_play_board()

  board = rotate(board, 80)
  board = transform(board, board.size, Image.PERSPECTIVE, coeffs)

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
  base = Image.new("RGB", mm_to_px(87 - PictureHelpCard.DX, 87 - PictureHelpCard.DX), (*background,))

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
  fn_card = PlayingCardBack("yellow").get_card()
  fn.paste(fn_card, mm_to_px(x2, y1), fn_card)

  for i in range(fns_count):
    transformed = transform_play_board(fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(fn, i)
    base.paste(transformed, mask=transformed)

  value = get_play_board()
  value_card = PlayingCardBack("blue").get_card()
  value.paste(value_card, mm_to_px(x1, y1), value_card)

  for i in range(values_count):
    transformed = transform_play_board(value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(value, i)
    base.paste(transformed, mask=transformed)

  used_value = get_play_board()
  used_value_card = ValueCard("green", values["green"][0]).get_card()
  used_value.paste(used_value_card, mm_to_px(x1, y2), used_value_card)

  for i in range(14 - values_count - 1):
    transformed = transform_play_board(used_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(used_value, i)
    base.paste(transformed, mask=transformed)

  if input_value_index is not None:
    input_value = get_play_board()
    input_value_card = ValueCard("green", values["green"][input_value_index]).get_card()
    input_value.paste(input_value_card, mm_to_px(x1, y2), input_value_card)

    i = 14 - values_count - 1
    transformed = transform_play_board(input_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(input_value, i)
    base.paste(transformed, mask=transformed)

  if output_value_index is not None:
    output_value = get_play_board()
    output_value_card = ValueCard("green", values["green"][output_value_index]).get_card()
    output_value.paste(output_value_card, mm_to_px(x2, y2), output_value_card)

    i = 0
    transformed = transform_play_board(output_value, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(output_value, i)
    base.paste(transformed, mask=transformed)

  for i in range(right_hand_count):
    right_hand = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    right_hand_tmp = Image.new("RGBA", mm_to_px(200, 200), (0, 0, 0, 0))
    right_hand_card = PlayingCardBack("yellow").get_card()
    right_hand_tmp.paste(right_hand_card, mm_to_px(50, 50), right_hand_card)
    # right_hand_tmp = resize(right_hand_tmp, (2 * right_hand_tmp.size[0], 2 * right_hand_tmp.size[1]))
    right_hand_tmp = rotate(right_hand_tmp, 13 + (-i - 1) * 8,
                            expand=False, center=mm_to_px((Card.base_width + 50, 50)))
    right_hand.paste(right_hand_tmp, mm_to_px(0, 80), right_hand_tmp)
    right_hand = rotate(right_hand, 180)

    coeffs = find_coefficients(
      [
        (mm_to_px(140), mm_to_px(20)),
        (right_hand.size[0] - mm_to_px(20), mm_to_px(40)),
        (right_hand.size[0] - mm_to_px(20), right_hand.size[1] - mm_to_px(130)),
        (mm_to_px(160), right_hand.size[1] - mm_to_px(140))
      ],
      [(0, 0), (right_hand.size[0], 0), (right_hand.size[0], right_hand.size[1]), (0, right_hand.size[1])]
    )
    right_hand = transform(right_hand, right_hand.size, Image.PERSPECTIVE, coeffs)
    scale = 1.5
    right_hand = resize(right_hand, (int(right_hand.width / scale), int(right_hand.height / scale)))
    base.paste(right_hand, mm_to_px(-110 / scale + 23, -30 / scale + 2), mask=right_hand)

  for i in range(len(used_fn_indexes)):
    used_fn = get_play_board()
    used_fn_card = FunctionCard("green", get_rules()["green"][used_fn_indexes[i]]).get_card()
    used_fn_card = rotate(used_fn_card, randint(0, 360))

    used_fn.paste(used_fn_card, mm_to_px(x1 / 2 + x2 / 2 - 5, y2 + 30), used_fn_card)

    transformed = transform_play_board(used_fn, i - 0.5)
    base.paste(blank, mask=transformed)
    transformed = transform_play_board(used_fn, i)
    base.paste(transformed, mask=transformed)

  for i in range(front_played_count):
    i += 1
    front_player_fn = get_play_board()
    front_player_fn_card = PlayingCardBack("yellow").get_card()
    front_player_fn_card = rotate(front_player_fn_card, 97 + 10 * -i)
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
    right_player_fn_card = PlayingCardBack("yellow").get_card()
    right_player_fn_card = rotate(right_player_fn_card, 51 + 8 * -i)
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
    front_hand_card = ValueCard("green", values["green"][0]).get_card()
    front_hand_tmp.paste(front_hand_card, mm_to_px(50, 50), front_hand_card)
    # front_hand_tmp = resize(front_hand_tmp, (2 * front_hand_tmp.size[0], 2 * front_hand_tmp.size[1]))
    front_hand_tmp = rotate(front_hand_tmp, -2 + (-i - 1) * 5, expand=False,
                            center=mm_to_px((Card.base_width + 50, Card.base_height + 50)))
    front_hand.paste(front_hand_tmp, mm_to_px(0, 0), front_hand_tmp)

    coeffs = get_main_plane_coeffs(front_hand.size, .9, i)
    front_hand = transform(front_hand, front_hand.size, Image.PERSPECTIVE, coeffs)
    scale = 2
    front_hand = resize(front_hand, (int(front_hand.width / scale), int(front_hand.height / scale)))
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
