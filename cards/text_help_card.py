from PIL import ImageDraw

from cards.help_card import HelpCard
from colors import getrgb
from image_lib.fonts import get_font
from image_lib.rendering import mm_to_px
from source_code_helpers import get_source_code_coloring, get_source_code_position_n_size


class TextHelpCard(HelpCard):
  def __init__(self, help_text):
    self.title, self.source_code = help_text.split('\n', 1)
    super().__init__(self.get_color())

  def get_color(self):
    return "cyan" if "PLAY THIS GAME" in self.title else "magenta"

  def get_card(self):
    card = super().get_card()
    draw = ImageDraw.Draw(card)

    font = get_font(13)
    W, H = card.size
    w, h = draw.textsize(self.title, font)
    colors = get_source_code_coloring(self.title)
    for color in colors:
      draw.text((W - mm_to_px(6) - w, mm_to_px(5)), colors[color], font=font, fill=getrgb(color))

    sc_size = get_source_code_position_n_size(card, self.source_code, draw)
    font = get_font(sc_size)
    w, h = draw.textsize(self.source_code, font, spacing=mm_to_px(0.6))
    colors = get_source_code_coloring(self.source_code)

    for color in colors:
      draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(2)), colors[color], font=font, fill=getrgb(color),
                spacing=mm_to_px(0.8))

    return card
