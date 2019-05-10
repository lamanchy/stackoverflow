import functools

from PIL import Image, ImageDraw

from colors import getrgb
from pil_quality_pdf.rendering import mm_to_px


class Card(object):
  base_width = 87
  base_height = 57
  base_size = (87, 57)

  def __init__(self, width, height, is_round):
    self.width = width
    self.height = height
    self.is_round = is_round

  @staticmethod
  def empty_card():
    return Card(0, 0, False)

  def size(self, dx=0, dy=0):
    return self.width + dx, self.height + dy

  def is_empty(self):
    return self.width == 0 or self.height == 0

  def get_card(self):
    card = self.get_blank()
    if not self.is_empty():
      self.paste_centered_rectangle(card, 0, "true_black")
      self.paste_centered_rectangle(card, 6, "lighter_black")
      self.paste_centered_rectangle(card, 8, "black")
    return card

  def paste_centered_rectangle(self, card, delta, color):
    radius = 10
    radius -= delta
    if delta != 0: radius += 2
    if not self.is_round: radius = 0
    rectangle = self.get_round_rectangle(self.size(-delta, -delta), color, radius)
    card.paste(rectangle, mm_to_px(delta / 2, delta / 2), mask=rectangle)

  @staticmethod
  @functools.lru_cache(None)
  def get_round_rectangle(size, color, radius):
    if isinstance(color, str): color = getrgb(color)
    if not isinstance(color, tuple): color = tuple(color)

    rectangle = Image.new('RGBA', mm_to_px(size), (*color, 0))
    draw = ImageDraw.Draw(rectangle)
    draw.rectangle(mm_to_px(radius / 2, 0, size[0] - (radius / 2), size[1]), fill=color)
    draw.rectangle(mm_to_px(0, radius / 2, size[0], size[1] - (radius / 2)), fill=color)
    draw.ellipse(mm_to_px(0, 0, radius, radius), fill=color)
    draw.ellipse(mm_to_px(size[0] - radius, 0, size[0], radius), fill=color)
    draw.ellipse(mm_to_px(0, size[1] - radius, radius, size[1]), fill=color)
    draw.ellipse(mm_to_px(size[0] - radius, size[1] - radius, size[0], size[1]), fill=color)

    return rectangle

  def get_blank(self):
    return Image.new("RGBA", mm_to_px(self.size()), (0, 0, 0, 0))
