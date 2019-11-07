from PIL import ImageDraw

from cards.card_face import CardFace
from cards.colored_card import ColoredCard
from colors import getrgb
from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import mm_to_px


class BackCard(ColoredCard):
  def __init__(self, width, height, is_round, color):
    super().__init__(width, height, is_round, CardFace.BACK, color)

  def blendified_color(self, **kwargs):
    return super().blendified_color(1.2, 100)

  def get_card(self):
    card = super().get_card()

    border_color = self.blendified_color()

    for delta, color in [(6, border_color), (7, "lighter_black"), (8, "black")]:
      self.paste_centered_rectangle(card, delta, color)

    self.write_logo(card)
    return card

  def write_logo(self, card):
    draw = ImageDraw.Draw(card)
    text = "Stack Overflow"
    W, H = mm_to_px(self.size())
    font = get_font(20)
    w, h = draw.textsize(text, font)
    draw.text(((W - w) // 2, (H - h) // 2), text, font=font, fill=getrgb(self.color))
