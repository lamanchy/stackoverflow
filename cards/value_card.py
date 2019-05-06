from PIL import ImageDraw

from cards.playing_card_front import PlayingCardFront
from colors import getrgb
from image_lib.fonts import get_font
from image_lib.rendering import mm_to_px
from source_code_helpers import get_source_code_coloring


class ValueCard(PlayingCardFront):
  def __init__(self, color, value):
    super().__init__(color)
    self.value = value

  def get_card(self):
    value = self.value[1]
    card = super().get_card()
    draw = ImageDraw.Draw(card)
    font = get_font(50)
    W, H = mm_to_px(self.size())
    w, h = draw.textsize(value, font)
    if value[0] in '-':
      w += draw.textsize('-', font)[0]

    colors = get_source_code_coloring(value)
    for color in colors:
      draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)),
                colors[color], font=font, fill=getrgb(color), spacing=mm_to_px(0.8))

    return card
