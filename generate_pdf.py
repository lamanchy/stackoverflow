# -*- coding: utf-8 -*-
import random
import sys
from datetime import datetime
from math import ceil

from PIL import Image

from cards.card import Card
from cards.two_sided_card import TwoSidedCard
from help_cards import get_all_help_cards
from image_lib.rendering import mm_to_px, PdfWriter
from rules import get_all_functions
from values import get_all_values

random.seed(10)

if __name__ == "__main__":
  cards = []
  counter = 0

  with PdfWriter("stack_overflow") as writer:
    def generate_pdf(last_time=False):
      if len(cards) < 10 and (not last_time or len(cards) == 0):
        return

      front_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
      back_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
      base_point = int(mm_to_px(210) / 2 - mm_to_px(Card.base_width) - mm_to_px(.05)), \
                   int(mm_to_px(297) / 2 - 2.5 * mm_to_px(Card.base_height) - mm_to_px(.2))

      for i, card in enumerate(cards[:10]):
        global counter
        counter += 1
        print("{} Generating {}. card".format(datetime.now(), counter))
        sys.stdout.flush()

        card = card.get_card()
        if card[0].size[0] == 0: continue
        offset_x = mm_to_px(Card.base_width + .1) if i % 2 == 1 else 0
        offset_y = mm_to_px(Card.base_height + .1) * (i // 2)

        front_canvas.paste(card[0], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[0])
        offset_x = mm_to_px(Card.base_width + .1) if i % 2 == 0 else 0
        background = Card.get_round_rectangle((
          (card[1].size[0] // mm_to_px(Card.base_width)) * Card.base_width + 4,
          (card[1].size[1] // mm_to_px(Card.base_height)) * Card.base_height + 4), "true_black", 10)
        back_canvas.paste(background, (base_point[0] + offset_x - mm_to_px(2), base_point[1] + offset_y - mm_to_px(2)),
                          mask=background)
        back_canvas.paste(card[1], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[1])

      writer.write(front_canvas)
      writer.write(back_canvas)

      for i in range(min(len(cards), 10)):
        cards.pop(0)


    def get_card():
      for i, function_card in enumerate(get_all_functions()):
        yield function_card

      for i, value_card in enumerate(get_all_values()):
        yield value_card

      while True:
        yield TwoSidedCard.empty_card()


    card_generator = get_card()

    for page in range(int(ceil(len(get_all_help_cards()) / 4))):
      for i, help_card in enumerate(get_all_help_cards()[page * 4:page * 4 + 4]):
        cards.append(help_card)
        if i in [1, 3]:
          for _ in range(2):
            cards.append(TwoSidedCard.empty_card())
          if i == 3:
            for _ in range(2):
              cards.append(card_generator.__next__())
        generate_pdf(False)

    while True:
      card = card_generator.__next__()
      if card.is_empty(): break
      cards.append(card)
      generate_pdf(False)

    generate_pdf(True)
