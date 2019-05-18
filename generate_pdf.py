# -*- coding: utf-8 -*-
import random
import sys
from datetime import datetime
from math import ceil

from PIL import Image

from cards.card import Card
from cards.two_sided_card import TwoSidedCard
from help.green_tutorial import green_tutorial
from help.red_tutorial import red_tutorial
from pil_quality_pdf.rendering import mm_to_px, PdfWriter


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

      writer.write(front_canvas)
      writer.write(back_canvas)


def prepare_help_cards_to_print(help_cards):
  while len(help_cards) % 4 != 0: help_cards.append(Card.empty_card())

  # brochure = help_cards
  brochure = []
  while len(help_cards) > 0:
    brochure.append(help_cards.pop(1))
    brochure.append(help_cards.pop(0))
    brochure.append(help_cards.pop(-2))
    brochure.append(help_cards.pop(-1))

  pairs = [TwoSidedCard(brochure[2 * i], brochure[2 * i + 1]) for i in range(len(brochure) // 2)]
  # pairs = [TwoSidedCard(brochure[i], Card.empty_card()) for i in range(len(brochure))]
  cards = []
  for page in range(int(ceil(len(pairs) / 4))):
    for i, help_card in enumerate(pairs[page * 4:page * 4 + 4]):
      cards.append(help_card)
      if i in [1, 3]:
        for _ in range(i + 1):
          cards.append(TwoSidedCard.empty_card())

  return cards


if __name__ == "__main__":
  # generate_pdf("stack_overflow_cards", get_all_functions() + get_all_values())

  tutorial_cards = green_tutorial + list(reversed(red_tutorial))

  generate_pdf("stack_overflow_tutorial", prepare_help_cards_to_print(tutorial_cards))
  # generate_pdf("stack_overflow_functions", prepare_help_cards_to_print(function_tutorial))
