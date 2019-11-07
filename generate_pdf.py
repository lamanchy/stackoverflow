# -*- coding: utf-8 -*-
import random
import sys
from datetime import datetime
from importlib import reload
from math import ceil, sqrt

from PIL import Image, ImageDraw
from PIL.Image import FLIP_LEFT_RIGHT

from cards.back_card import BackCard
from cards.card import Card
from cards.function_card import FunctionCard
from cards.two_sided_card import TwoSidedCard
from colors import getrgb
from language import set_language, LANGUAGES
from pil_quality_pdf.rendering import mm_to_px, PdfWriter, px_to_mm

BROCHURE = True

try:
  from local_generate_settings import *
except ImportError:
  pass


def generate_pdf(name, cards):
  random.seed(10)

  with PdfWriter(name) as writer:
    counter = 0

    space = .05
    base_point = int(mm_to_px(210) / 2 - mm_to_px(Card.base_width) - mm_to_px(space / 2)), \
                 int(mm_to_px(297) / 2 - 2.5 * mm_to_px(Card.base_height) - mm_to_px(space * 2))

    while len(cards) > 0:
      front_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
      back_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
      for i in range(len(cards[:10])):
        card = cards.pop(0)
        counter += 1
        print("{} Generating {}. card".format(datetime.now(), counter))
        sys.stdout.flush()

        card = card.get_card()
        offset_x = mm_to_px(Card.base_width + space) if i % 2 == 1 else 0
        offset_y = mm_to_px(Card.base_height + space) * (i // 2)

        if card[0].size[0] > 0:
          front_canvas.paste(card[0], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[0])
        offset_x = mm_to_px(Card.base_width + space) if i % 2 == 0 else 0
        background = Card.get_round_rectangle((
          (card[1].size[0] // mm_to_px(Card.base_width)) * Card.base_width + 4,
          (card[1].size[1] // mm_to_px(Card.base_height)) * Card.base_height + 4), "true_black", 0)

        if card[1].size[0] > 0:
          back_canvas.paste(background,
                            (base_point[0] + offset_x - mm_to_px(2), base_point[1] + offset_y - mm_to_px(2)),
                            mask=background)
          back_canvas.paste(card[1], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[1])

      if not all([p == (255, 255, 255) for p in front_canvas.getdata()]):
        writer.write(front_canvas)
      if not all([p == (255, 255, 255) for p in back_canvas.getdata()]):
        writer.write(back_canvas)


def prepare_help_cards_to_print(help_cards):
  while len(help_cards) % 4 != 0: help_cards.append(Card.empty_card())

  brochure = help_cards
  if BROCHURE:
    brochure = []
    while len(help_cards) > 0:
      brochure.append(help_cards.pop(1))
      brochure.append(help_cards.pop(0))
      brochure.append(help_cards.pop(-2))
      brochure.append(help_cards.pop(-1))

  pairs = [TwoSidedCard(brochure[2 * i], brochure[2 * i + 1]) for i in range(len(brochure) // 2)]
  if not BROCHURE:
    pairs = [TwoSidedCard(brochure[i], Card.empty_card()) for i in range(len(brochure))]
  cards = []
  for page in range(int(ceil(len(pairs) / 4))):
    for i, help_card in enumerate(pairs[page * 4:page * 4 + 4]):
      cards.append(help_card)
      if i in [1, 3]:
        for _ in range(i + 1):
          cards.append(TwoSidedCard.empty_card())

  return cards


import help.green_tutorial
import help.red_tutorial
import rules
import values
import help.function_tutorial


def dashed_line(draw, xy, fill, width):
  dir = (xy[1][0] - xy[0][0], xy[1][1] - xy[0][1])
  total_dist = sqrt(pow(dir[0], 2) + pow(dir[1], 2))
  step_dist = mm_to_px(1)
  step = (dir[0] * step_dist / total_dist, dir[1] * step_dist / total_dist)
  dist = 0
  pos = xy[0]
  while dist + step_dist < total_dist:
    draw.line((pos, (pos[0] + step[0], pos[1] + step[1])), fill, width)
    pos = (pos[0] + 2 * step[0], pos[1] + 2 * step[1])
    dist += 2 * step_dist

  if dist < total_dist:
    draw.line((pos, xy[1]), fill, width)


def generate_box(name):
  with PdfWriter(name) as f:
    extra_space_around_cards = 1
    extra_space_because_of_how_box_is_folded = 2
    for diff in [0, 1]:
      w = mm_to_px(Card.base_width + diff + extra_space_around_cards)
      l = mm_to_px((Card.base_height + diff) * 2 + extra_space_around_cards + extra_space_because_of_how_box_is_folded)
      h = mm_to_px(22)
      mx = max(w // 2, h * 2)
      mn = min(w // 2, h * 2)
      margin = mm_to_px(30)

      for i in range(2):
        cropping = mm_to_px(2) if i == 0 else 0

        page = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
        draw = ImageDraw.Draw(page)
        color = getrgb("black") if diff == 0 else getrgb("true_black")
        draw.rectangle((
          (margin - cropping, margin + mx - w // 2 - cropping),
          (margin + h + w + h + cropping, margin + mx + l + w // 2 + cropping)
        ), color)
        draw.rectangle((
          (margin + h - cropping, margin + mx - h * 2 - cropping),
          (margin + h + w + cropping, margin + mx + l + h * 2 + cropping)
        ), color)

        if i == 0 and diff == 1:
          card = BackCard(px_to_mm(w), px_to_mm(l), True, "orange").get_card()
          page.paste(card, (margin + h, margin + mx), mask=card)

        if i == 1:
          line_color = getrgb("white")
          line_width = mm_to_px(.05)
          draw.line(((margin + h, margin + mx + l + mn), (margin + h, margin + mx + l),), line_color, line_width)
          draw.line(((margin + h + w, margin + mx + l), (margin + h + w, margin + mx + l + mn),), line_color,
                    line_width)
          draw.line(((margin + h + w, margin + mx - mn), (margin + h + w, margin + mx),), line_color, line_width)
          draw.line(((margin + h, margin + mx - mn), (margin + h, margin + mx),), line_color, line_width)

          dashed_line(draw, ((margin + h, margin + mx - h), (margin + h + w, margin + mx - h)), line_color, line_width)

          dashed_line(draw, ((margin, margin + mx), (margin + h, margin + mx)), line_color, line_width)
          dashed_line(draw, ((margin + h, margin + mx), (margin + h + w, margin + mx)), line_color, line_width)
          dashed_line(draw, ((margin + h + w, margin + mx), (margin + h + w + h, margin + mx)), line_color, line_width)

          dashed_line(draw, ((margin, margin + mx + l), (margin + h, margin + mx + l)), line_color, line_width)
          dashed_line(draw, ((margin + h, margin + mx + l), (margin + h + w, margin + mx + l)), line_color, line_width)
          dashed_line(draw, ((margin + h + w, margin + mx + l), (margin + h + w + h, margin + mx + l)), line_color,
                      line_width)

          dashed_line(draw, ((margin + h, margin + mx + l + h), (margin + h + w, margin + mx + l + h)), line_color,
                      line_width)

          dashed_line(draw, ((margin + h, margin + mx), (margin + h, margin + mx + l)), line_color, line_width)
          dashed_line(draw, ((margin + h + w, margin + mx), (margin + h + w, margin + mx + l)), line_color, line_width)

        if i == 1:
          page = page.transpose(FLIP_LEFT_RIGHT)
        f.write(page)


if __name__ == "__main__":
  for language in LANGUAGES:
    n = datetime.now()
    set_language(language)

    reload(help.green_tutorial)
    reload(help.red_tutorial)
    reload(rules)
    reload(values)
    reload(help.function_tutorial)

    if BROCHURE:
      tutorial_cards = help.green_tutorial.green_tutorial + list(reversed(help.red_tutorial.red_tutorial))
    else:
      tutorial_cards = help.green_tutorial.green_tutorial + help.red_tutorial.red_tutorial
      for card in tutorial_cards: card.is_upside_down = False

    generate_pdf(f"stack_overflow_cards_{language}", FunctionCard.get_all_functions() + values.get_all_values())
    generate_pdf(f"stack_overflow_tutorial_{language}", prepare_help_cards_to_print(tutorial_cards))
    generate_pdf(f"stack_overflow_functions_{language}",
                 prepare_help_cards_to_print(help.function_tutorial.function_tutorial))

    generate_box(f"stack_overflow_box_{language}")

    print(f"{language} generation took:", datetime.now() - n)
