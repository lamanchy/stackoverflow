from PIL import ImageDraw

from cards.help_card import HelpCard
from colors import getrgb
from pil_quality_pdf.fonts import get_font


class TitleHelpCard(HelpCard):
  def __init__(self, title, subtitle, color):
    super().__init__(color)
    self.subtitle = subtitle
    self.title = title
    self.is_upside_down = False

  def get_card(self):
    card = super().get_card()

    draw = ImageDraw.Draw(card)

    font = get_font(20)
    size = draw.textsize(self.title, font)
    draw.text(((card.size[0] - size[0]) / 2, (card.size[1] / 2 - size[1])), self.title, fill=getrgb("white"), font=font,
              align="center")

    font = get_font(15)
    size = draw.textsize(self.subtitle, font)
    draw.text(((card.size[0] - size[0]) / 2, card.size[1] / 2 + size[1] * 0.5), self.subtitle, fill=getrgb("white"),
              font=font, align="center")

    if self.is_upside_down:
      card = card.rotate(180)
    return card
