import logging

from PIL import ImageDraw

from cards.help_card import HelpCard
from colors import getrgb
from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import mm_to_px
from source_code_helpers import get_source_code_coloring, get_source_code_position_n_size


class TextHelpCard(HelpCard):
  delta = mm_to_px(10)
  title_size = 14
  text_size = 11

  def __init__(self, color, title, text):
    self.should_resize = False
    self.title = title
    self.text = text
    self.title = self.title.strip()
    self.top = self.delta
    super().__init__(color)

    self.check_sizes()
    self.is_upside_down = False

  def has_title(self):
    return len(self.title) > 0

  def get_card(self):
    card = super().get_card()
    draw = ImageDraw.Draw(card)

    if self.has_title():
      font = get_font(self.title_size)
      colors = get_source_code_coloring(self.title)
      for color in colors:
        draw.text((mm_to_px(10), self.top), colors[color], font=font, fill=getrgb(color))

      height = draw.textsize("A", font)[1]

      self.top += height * 2.05

    if self.has_title() or not self.should_resize:
      font = get_font(self.text_size)
      colors = get_source_code_coloring(self.text)
      for color in colors:
        draw.text((mm_to_px(10), self.top), colors[color], font=font, fill=getrgb(color), spacing=mm_to_px(.8))
    else:
      sc_size = get_source_code_position_n_size(card, self.text, draw)
      font = get_font(sc_size)
      w, h = draw.textsize(self.text, font, spacing=mm_to_px(0.6))
      colors = get_source_code_coloring(self.text)

      for color in colors:
        draw.text((mm_to_px(10), (card.size[1] - h) // 2 - mm_to_px(2)), colors[color], font=font, fill=getrgb(color),
                  spacing=mm_to_px(0.8))

    if self.is_upside_down:
      card = card.rotate(180)
    return card

  def check_sizes(self):
    if len(self.title) > 31:
      logging.warning(f"Title {self.title} is too long! (31 chars max)")

    lines = self.text.split("\n")
    lines.sort(reverse=True, key=lambda line: len(line))
    line = lines[0]
    if len(line) > 42:
      logging.warning(f"Line {line} is too long! (42 chars max)")

    if len(lines) > (27 if self.has_title() else 29):
      logging.warning(f"There is too many lines ({len(lines)}), max. lines count is 27 (29), in {self}")

  def __repr__(self):
    if self.has_title():
      return self.title

    return self.text.split("\n")[0]
