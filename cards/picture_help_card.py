from PIL import Image, ImageDraw

from cards.help_card import HelpCard
from colors import getrgb
from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import mm_to_px


class PictureHelpCard(HelpCard):
  DX = 20.0

  def __init__(self, heading, text, picture):
    super().__init__("green")
    self.heading = heading
    self.text = text
    self.picture = picture

  def has_picture(self):
    return self.picture is not None

  def box_draw(self, card, move, picture=None, color=None):
    assert picture is not None or color is not None

    box_size = mm_to_px((self.width - move, self.width - move))
    if picture is None:
      picture = Image.new('RGB',
                          box_size,
                          getrgb(color))

    picture = picture.crop((0, 0,) + box_size)

    card.paste(picture, mm_to_px(move / 2, move / 2))

  def get_card(self):
    card = super().get_card()

    if self.has_picture():
      self.box_draw(card, self.DX - .5, color="grey")
      self.box_draw(card, 20, self.picture())

    draw = ImageDraw.Draw(card)
    font = get_font(15)
    x = self.DX / 2 + 2
    y = self.width - x / 2
    if not self.has_picture(): y = x
    text_color = getrgb("white")
    draw.text(mm_to_px(x, y), text=self.heading, fill=text_color, font=font, spacing=mm_to_px(0.8))

    font = get_font(11)
    y += 7
    draw.text(mm_to_px(x, y), text=self.text, fill=text_color, font=font, spacing=mm_to_px(0.8))

    return card
