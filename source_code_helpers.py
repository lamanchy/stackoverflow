import inspect
import re

from cards.card import Card
from colors import color_regexes
from pil_quality_pdf.fonts import get_font
from pil_quality_pdf.rendering import mm_to_px


def get_source_code(fn):
  source_code = inspect.getsource(fn)

  # remove leading and ending spaces
  source_code = source_code.strip().split('\n')

  for i in range(len(source_code) - 1, -1, -1):
    if "# DEBUG this line wont be printed" in source_code[i]:
      source_code = source_code[:i] + source_code[i + 1:]

    if source_code[i].startswith('@'):
      source_code = source_code[:i] + source_code[i + 1:]

  source_code = '\n'.join(source_code)

  if source_code.startswith("lambda") and source_code[-1] == ',':
    source_code = source_code[:-1]

  return source_code


def get_source_code_name(source_code):
  if not isinstance(source_code, str):
    source_code = get_source_code(source_code)

  source_code = source_code.split('\n')[0]
  colloring = get_source_code_coloring(source_code)

  if source_code.startswith("def"):
    start = len("def ")
    end = len(source_code) - 1
    while source_code[end] != '(':
      end -= 1

  else:
    start = len("lambda x: ")
    end = len(source_code)

  source_code = source_code[start:end]
  for color in colloring:
    colloring[color] = colloring[color][start:end]

  return source_code, colloring


def colorify_string(string):
  colors = [color_regexes[0][1] for _ in range(len(string))]
  for regex, color in color_regexes:
    for match in re.finditer(regex, string):
      if len(match.groups()) > 0:
        span = match.span(1)
      else:
        span = match.span()

      for i in range(*span):
        colors[i] = color

  return colors


def get_source_code_coloring(string):
  colors = colorify_string(string)

  result = {}
  for color in set(colors):
    result[color] = ""
    for char, char_color in zip(string, colors):
      if char in "ěščř": char = "⧫"  # ●∙
      if not re.match(r'\s', char) and char_color != color:
        char = " "
      result[color] += char

  return result


# TODO i should refactor this
def get_source_code_position_n_size(card, source_code, draw):
  # width is exactly half the height

  min_font_size = 1
  max_font_size = 25
  height_multipler = card.size[1] // mm_to_px(Card.base_height)
  available_size = list((card.size[0] - mm_to_px(10), card.size[1] - mm_to_px(5 * (height_multipler - 1) + 30)))

  while True:
    size = draw.textsize(source_code, get_font(min_font_size + 1), spacing=mm_to_px(.13))

    if size[0] >= available_size[0] or size[1] >= available_size[1] or min_font_size == max_font_size:
      if (height_multipler == 1 and min_font_size < 15) or (height_multipler == 2 and min_font_size < 11):
        print("too small font size, fn {}, font size {}".format(source_code.split('\n')[0], min_font_size))
        print(size, available_size)
      return min_font_size

    min_font_size += 1
    available_size[0] *= .99
