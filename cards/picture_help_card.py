import os

from PIL import Image

from cards.text_help_card import TextHelpCard
from colors import getrgb
from language import get_language
from pil_quality_pdf.rendering import mm_to_px
from pil_quality_pdf.transformation import resize


class PictureHelpCard(TextHelpCard):
  DX = 20.0

  def __init__(self, color, title, text, picture_getter):
    super().__init__(color, title, text)
    self.picture_getter = picture_getter
    self.id = None

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

    self.paste_arrows(card)

    return card

  def paste_arrows(self, card):
    id = f"{self.id}-01.png"
    candidates = [file for file in os.listdir(f"help/arrows/{get_language()}") if id == file]
    if len(candidates) != 1:
      print(f"There is no arrow for {self.title}, id: {id}")
      exit(1)
    file = candidates[0]

    im = Image.open(f"help/arrows/{get_language()}/" + file)

    im = resize(im, card.size)

    card.paste(im, mask=im)
