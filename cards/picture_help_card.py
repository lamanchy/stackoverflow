from PIL import Image

from cards.text_help_card import TextHelpCard
from colors import getrgb
from pil_quality_pdf.rendering import mm_to_px


class PictureHelpCard(TextHelpCard):
  DX = 20.0

  def __init__(self, color, title, text, picture_getter):
    super().__init__(color, title, text)
    self.picture_getter = picture_getter

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
    self.top = mm_to_px(self.width - 7)

    card = super().get_card()

    self.box_draw(card, self.DX - .5, color="grey")
    self.box_draw(card, 20, self.picture_getter())

    return card
