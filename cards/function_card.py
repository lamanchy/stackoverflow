from PIL import ImageDraw

from cards.playing_card_back import PlayingCardBack
from cards.playing_card_front import PlayingCardFront
from cards.two_sided_card import TwoSidedCard
from colors import getrgb
from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import mm_to_px
from rules import get_rules
from source_code_helpers import get_source_code_position_n_size, get_source_code_coloring, get_source_code


class FunctionCard(PlayingCardFront):
  def __init__(self, color, rule):
    super().__init__(color)
    self.rule = rule

  def get_card(self):
    source_code = get_source_code(self.rule)
    colors = get_source_code_coloring(source_code)

    card = super().get_card()
    draw = ImageDraw.Draw(card)

    sc_size = get_source_code_position_n_size(card, source_code, draw)
    font = get_font(sc_size)

    W, H = mm_to_px(self.size())
    w, h = draw.textsize(source_code, font)
    for color in colors:
      draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(1)),
                colors[color], font=font, fill=getrgb(color), spacing=mm_to_px(0.8))

    return card

  @staticmethod
  def get_all_functions():
    fns = []
    for color in ["green", "yellow", "red", "white"]:
      for fn in get_rules()[color]:
        fns.append(TwoSidedCard(FunctionCard(color, fn), PlayingCardBack("yellow")))

    return fns
