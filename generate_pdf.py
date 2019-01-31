# -*- coding: utf-8 -*-
import inspect
import os
import re
from math import ceil
from numbers import Number

from PIL import Image, ImageFont, ImageDraw, ImageColor
from PIL.Image import ANTIALIAS

from help_cards import get_all_help_cards
from rules import get_rules, get_all_functions
from values import get_all_values

FONT = "fonts/DejaVuSansMono.ttf"
FONT_BOLD = "fonts/DejaVuSansMono-Bold.ttf"

ANTIALIASING = 3  # do not set bigger that 32 :D
RESOLUTION_DPI = 300
TEXTURE = "textures/moulin.png"
TEXTURE = "textures/slash_it.png"
TEXTURE = "textures/what-the-hex-dark.png"
# TEXTURE = "textures/zig zag wool.png"
CARD_SIZE_MM = (87, 57)
# CARD_SIZE_MM = (93, 69)


def do_antialiasing(img):
  return img.resize((img.size[0] // ANTIALIASING, img.size[1] // ANTIALIASING), ANTIALIAS)


def show(img):
  do_antialiasing(img).show()

# dasda


def mm_to_px(*args):
  x = args
  if len(args) == 1:
    x = args[0]
  if isinstance(x, int) or isinstance(x, float):
    return int(RESOLUTION_DPI * ANTIALIASING * 0.03937 * x)

  return type(x)([mm_to_px(i) for i in x])


def get_font(size, font=FONT):
  return ImageFont.truetype(font, size=size * RESOLUTION_DPI * ANTIALIASING // 100)


color_codes = {
  "black": "#2b2b2b",
  "true_black": "#000000",
  "lighter_black": "#313335",
  "white": "rgb(212,225,240)",
  "true_white": "#FFFFFF",
  "blue": "rgb(102,180,250)",
  "violet": "rgb(169,168,255)",
  "orange": "rgb(230,142,71)",
  "yellow": "#FFC66D",
  "green": "rgb(100,183,70)",
  "grey": "rgb(166,166,166)",
  "red": "rgb(216,69,65)",
  "cyan": "rgb(82,187,186)",
  "magenta": "rgb(194,158,211)",
}


def get_source_code(fn):
  source_code = inspect.getsource(fn)

  # remove leading and ending spaces
  source_code = source_code.strip().split('\n')

  for i in range(len(source_code)-1, -1, -1):
    if "# DEBUG this line wont be printed" in source_code[i]:
      source_code = source_code[:i] + source_code[i+1:]

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


card_colors_to_real_colors = {
  "green": "green",
  "yellow": "yellow",
  "red": "red",
  "black": "white",
  "magenta": "magenta",
  "cyan": "cyan",
}

color_regexes = [
  (r".*", "white"),  # default color
  (r"(?:\W|^)(\d+)", "blue"),
  (r"(-|\.)(?=\d)", "blue"),
  (r"(√|π|pi|inf)", "blue"),
  (
    r'(?:^|\s|\(|\[)(round|range|abs|max|min|floor|len|gcd|lcm|is_prime|sqrt|ceil|log2|sin|int|str'
    r'|pow|float|eval|sign|isnan|input|get_all_cards|shuffle|all|enumerate'
    r'|isinf|ZeroDivisionError|ValueError|TypeError|RecursionError|Exception)(?=\(|:|\s|\)|,|$)',
    "violet"),
  (r'(?:^|\s|=)(lambda|def|if|while|and|or|else|elif|for|in|return|None|global'
   r'|is|except|try|as)(?=\W|:|\))', "orange"),
  (r'def (\w*)', "yellow"),
  (r"'[^'\n]*'", "green"),
  (r'"[^"]*"', "green"),
  (r'#\s.*', "grey"),
  (r'ě', "green"),
  (r'š', "yellow"),
  (r'č', "red"),
  (r'ř', card_colors_to_real_colors["black"]),
]


def get_source_code_coloring(string):
  colors = [color_regexes[0][1] for i in range(len(string))]
  for regex, color in color_regexes:
    for match in re.finditer(regex, string):
      if len(match.groups()) > 0:
        span = match.span(1)
      else:
        span = match.span()

      for i in range(*span):
        colors[i] = color

  result = {}

  for color in set(colors):
    result[color] = ""
    for char, char_color in zip(string, colors):
      if char in "ěščř": char = "⧫" # ●∙
      if not re.match(r'\s', char) and char_color != color:
        char = " "
      result[color] += char

  return result


def apply_texture(image, texture):
  texture = Image.open(texture)
  texture = texture.resize((texture.size[0] * ANTIALIASING, texture.size[1] * ANTIALIASING))
  texture = texture.point(lambda p: p * 2)
  for x in range(0, image.size[0], texture.size[0]):
    for y in range(0, image.size[1], texture.size[1]):
      image.paste(texture, (x, y), mask=image.crop((x, y, x + texture.size[0], y + texture.size[1])))


def get_round_rectangle(size=CARD_SIZE_MM, color="black", radius=10.0, texture=None):
  if isinstance(color, str): color = ImageColor.getrgb(color_codes[color])
  if not isinstance(color, tuple): color = tuple(color)
  rectangle = Image.new('RGBA', mm_to_px(size), (*color, 0))
  draw = ImageDraw.Draw(rectangle)
  draw.rectangle(mm_to_px(radius / 2, 0, size[0] - (radius / 2), size[1]), fill=color)
  draw.rectangle(mm_to_px(0, radius / 2, size[0], size[1] - (radius / 2)), fill=color)
  draw.ellipse(mm_to_px(0, 0, radius, radius), fill=color)
  draw.ellipse(mm_to_px(size[0] - radius, 0, size[0], radius), fill=color)
  draw.ellipse(mm_to_px(0, size[1] - radius, radius, size[1]), fill=color)
  draw.ellipse(mm_to_px(size[0] - radius, size[1] - radius, size[0], size[1]), fill=color)
  if texture is not None:
    apply_texture(rectangle, texture)

  return rectangle


def get_card_base(multipler=(1, 1)):
  size = (CARD_SIZE_MM[0]*multipler[0], CARD_SIZE_MM[1]*multipler[1])
  card = get_round_rectangle(size, "true_black")
  border = get_round_rectangle((size[0] - 6, size[1] - 6), "lighter_black", radius=6)
  card.paste(border, mm_to_px(3, 3), mask=border)
  background = get_round_rectangle((size[0] - 8, size[1] - 8), "black", radius=4)
  card.paste(background, mm_to_px(4, 4), mask=background)
  return card


def get_order_sign_n_color(order):
  sign = "♠"
  if order % 4 == 1: sign = u"♣"
  if order % 4 == 2: sign = u"♥"
  if order % 4 == 3: sign = u"♦"

  number = (8 + order) // 4
  if number == 11:
    number = "J"
  elif number == 12:
    number = "Q"
  elif number == 13:
    number = "K"
  elif number == 14:
    number = "A"
  else:
    number = str(number)
  return sign + number, "orange" if (order // 2) % 2 == 1 else "blue"


def get_card_base_with_color(order, color, multipler=(1, 1)):
  card = get_card_base(multipler)
  smaller_by = 0
  border_color = list(ImageColor.getrgb(color_codes[card_colors_to_real_colors[color]]))
  for i in range(len(border_color)): border_color[i] //= 1.5
  for i in range(len(border_color)): border_color[i] = int(border_color[i])
  border = get_round_rectangle((CARD_SIZE_MM[0]*multipler[0] - 7 - smaller_by, CARD_SIZE_MM[1]*multipler[1] - 7 - smaller_by), border_color, radius=5-smaller_by)
  card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 6, CARD_SIZE_MM[1] - 6), "lighter_black", radius=6)
  # card.paste(border, mm_to_px(4, 3), mask=border)
  background = get_round_rectangle((CARD_SIZE_MM[0]*multipler[0] - 8, CARD_SIZE_MM[1]*multipler[1] - 8), "black", radius=4)
  card.paste(background, mm_to_px(4, 4), mask=background)
  # background = get_round_rectangle((CARD_SIZE_MM[0] - 9, CARD_SIZE_MM[1] - 9), "black", radius=3)
  # card.paste(background, mm_to_px(4.5, 4.5), mask=background)
  # draw = ImageDraw.Draw(card)
  # base_size = 10
  # move_up = 3.5
  # move_left = 3.5
  # smaller_by = -.5
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes["lighter_black"])
  # smaller_by = .5
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes[card_colors_to_real_colors[color]])
  # smaller_by = 1
  # draw.ellipse(mm_to_px(
  #   move_left + smaller_by,
  #   CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
  #   base_size + move_left - smaller_by,
  #   CARD_SIZE_MM[1] - move_up - smaller_by
  # ), fill=color_codes["true_black"])

  # font = get_font(15, FONT_BOLD)
  # sign, color = get_order_sign_n_color(order)
  # w, _ = draw.textsize(sign, font)
  # _, h = draw.textsize("8", font)
  # draw.text(
  #   (
  #     mm_to_px(move_left + base_size // 2) - w // 2 - mm_to_px(.1),
  #     mm_to_px(CARD_SIZE_MM[1] - base_size // 2 - move_up) - h // 2 - mm_to_px(.45)
  #   ),
  #   sign, font=font, fill=color_codes[color])

  return card


def get_source_code_position_n_size(card, source_code, draw):
  # width is exactly half the height

  min_font_size = 1
  max_font_size = 25
  height_multipler = card.size[1] // mm_to_px(CARD_SIZE_MM[1])
  available_size = list((card.size[0] - mm_to_px(10), card.size[1] - mm_to_px(5*(height_multipler-1) + 30)))

  while True:
    size = draw.textsize(source_code, get_font(min_font_size + 1), spacing=mm_to_px(.13))

    if size[0] >= available_size[0] or size[1] >= available_size[1] or min_font_size == max_font_size:
      if (height_multipler == 1 and min_font_size < 15) or (height_multipler == 2 and min_font_size < 11):
        print("too small font size, fn {}, font size {}".format(source_code.split('\n')[0], min_font_size))
        print(size[0], available_size[0])
      return min_font_size

    min_font_size += 1
    available_size[0] *= .99


def get_fn_card_front(order, fn, color):
  source_code = get_source_code(fn)
  colors = get_source_code_coloring(source_code)

  card = get_card_base_with_color(order, color)
  base = Image.new("RGBA", mm_to_px(CARD_SIZE_MM), (0, 0, 0, 0))
  draw = ImageDraw.Draw(base)
  sc_size = get_source_code_position_n_size(card, source_code, draw)
  font = get_font(sc_size)
  W, H = mm_to_px(CARD_SIZE_MM)
  w, h = draw.textsize(source_code, font)

  for color in colors:
    draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(1)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))

  # name, name_colloring = get_source_code_name(fn)
  # font = get_font(10)
  # w, h = draw.textsize(name, font)
  #
  # for color in name_colloring:
  #   draw.text((mm_to_px(15), H - h - mm_to_px(5)), name_colloring[color], font=font, fill=color_codes[color])

  card.paste(base, mask=base)

  return card


def get_value_card_front(order, value, color):
  value = value[1]
  card = get_card_base_with_color(order, color)
  draw = ImageDraw.Draw(card)
  font = get_font(50)
  W, H = mm_to_px(CARD_SIZE_MM)
  w, h = draw.textsize(value, font)
  if value[0] in '-':
    w += draw.textsize('-', font)[0]

  # draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(3)), value, font=font, fill=color_codes["blue"])
  colors = get_source_code_coloring(value)
  for color in colors:
    draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))
  # draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), value, font=font, fill=color_codes["blue"])

  return card


def get_card_back(color):
  # card = get_card_base()
  # for i, text in enumerate(["Stack\n", "Overflow\n"]):
  #   invisible = Image.new('RGBA', mm_to_px(CARD_SIZE_MM), (0, 0, 0, 0))
  #   draw = ImageDraw.Draw(invisible)
  #   W, H = mm_to_px(CARD_SIZE_MM)
  #   # font = get_font(17)
  #   font = get_font(25)
  #   w, h = draw.textsize(text, font)
  #   draw.text(((W - w) // 2, (H - h) // 2 - mm_to_px(1)), text, font=font, fill=color_codes[color])
  #
  #   invisible = invisible.rotate(i*180)
  #   card.paste(invisible, mask=invisible)

  card = get_card_base()

  smaller_by = -2
  border_color = list(ImageColor.getrgb(color_codes[color]))
  for i in range(len(border_color)): border_color[i] /= 1.2
  for i in range(len(border_color)): border_color[i] = int(max(border_color[i] - 100, 0))
  # smaller_by = -7
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), border_color, radius=5-smaller_by)
  # card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # smaller_by = -6
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "true_black", radius=5-smaller_by)
  # card.paste(border, mm_to_px(3.5+smaller_by/2, 3.5+smaller_by/2), mask=border)
  # border = get_round_rectangle((CARD_SIZE_MM[0] - 6, CARD_SIZE_MM[1] - 6), "lighter_black", radius=6)
  # card.paste(border, mm_to_px(4, 3), mask=border)
  smaller_by = -1
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), border_color,
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)
  smaller_by = 0
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "lighter_black",
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)
  smaller_by = 1
  border = get_round_rectangle((CARD_SIZE_MM[0] - 7 - smaller_by, CARD_SIZE_MM[1] - 7 - smaller_by), "black",
                               radius=5 - smaller_by)
  card.paste(border, mm_to_px(3.5 + smaller_by / 2, 3.5 + smaller_by / 2), mask=border)

  draw = ImageDraw.Draw(card)
  text = "Stack Overflow"
  W, H = mm_to_px(CARD_SIZE_MM)
  font = get_font(20)
  w, h = draw.textsize(text, font)
  draw.text(((W - w) // 2, (H - h) // 2), text, font=font, fill=color_codes[color])
  return card.rotate(180)


def get_fn_card(order, fn, color):
  return get_fn_card_front(order, fn, color), get_card_back("yellow")


def get_help_card(help_text):
  title, source_code = help_text.split('\n', 1)
  # print(source_code)
  color = "cyan" if "PLAY THIS GAME" in title else "magenta"

  card = get_card_base_with_color(1, color, (1, 2))
  # card = get_card_base((1, 2))
  draw = ImageDraw.Draw(card)

  font = get_font(13)
  W, H = card.size
  w, h = draw.textsize(title, font)
  colors = get_source_code_coloring(title)
  for color in colors:
    draw.text((W - mm_to_px(6) - w, mm_to_px(5)), colors[color], font=font, fill=color_codes[color])

  sc_size = get_source_code_position_n_size(card, source_code, draw)
  font = get_font(sc_size)
  w, h = draw.textsize(source_code, font, spacing=mm_to_px(0.6))
  colors = get_source_code_coloring(source_code)

  for color in colors:
    draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(2)), colors[color], font=font, fill=color_codes[color], spacing=mm_to_px(0.8))

  return card


def get_value_card(order, value, color):
  return get_value_card_front(order, value, color), get_card_back("blue")


if __name__ == "__main__":
  cards = []
  is_this_first_page = True

  try:
    os.remove("stack_overflow.pdf")
  except FileNotFoundError:
    pass


  def generate_pdf(last_time=False):
    if len(cards) < 10 and (not last_time or len(cards) == 0):
      return

    front_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
    back_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
    base_point = int(mm_to_px(210) / 2 - mm_to_px(CARD_SIZE_MM[0]) - mm_to_px(.05)), \
                 int(mm_to_px(297) / 2 - 2.5 * mm_to_px(CARD_SIZE_MM[1]) - mm_to_px(.2))

    for i, card in enumerate(cards[:10]):
      if card[0].size[0] == 0: continue
      offset_x = mm_to_px(CARD_SIZE_MM[0] + .1) if i % 2 == 1 else 0
      offset_y = mm_to_px(CARD_SIZE_MM[1] + .1) * (i // 2)

      front_canvas.paste(card[0], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[0])
      offset_x = mm_to_px(CARD_SIZE_MM[0] + .1) if i % 2 == 0 else 0
      background = get_round_rectangle((
        (card[1].size[0] // mm_to_px(CARD_SIZE_MM[0]))*CARD_SIZE_MM[0]+2,
        (card[1].size[1] // mm_to_px(CARD_SIZE_MM[1]))*CARD_SIZE_MM[1]+2), "true_black")
      back_canvas.paste(background, (base_point[0] + offset_x - mm_to_px(1), base_point[1] + offset_y - mm_to_px(1)), mask=background)
      back_canvas.paste(card[1], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[1])

    def save_canvas(canvas):
      canvas = do_antialiasing(canvas)
      try:
        canvas.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
                    resolution=RESOLUTION_DPI, append=True)
      except IOError:
        canvas.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
                    resolution=RESOLUTION_DPI, append=False)

    save_canvas(front_canvas)
    save_canvas(back_canvas)

    for i in range(min(len(cards), 10)):
      cards.pop(0)

  # for i, (fn, c) in enumerate(get_all_functions()):
  #   print(c, get_source_code(fn))


  def get_card():
    # for i, (fn, c) in enumerate(get_all_functions()[0:2] + get_all_functions()[16:18] + get_all_functions()[-8:-6] + get_all_functions()[-2:]):
    # for i, (fn, c) in enumerate(get_all_functions()):
    #   yield get_fn_card(i, fn, c)

    # for i, (v, c) in enumerate(get_all_values()[0:2] + get_all_values()[16:18] + get_all_values()[-8:-6] + get_all_values()[-2:]):
    # for i, (v, c) in enumerate(get_all_values()):
    #     yield get_value_card(i, v, c)

    while True:
      yield (Image.new("RGB", (0, 0)), Image.new("RGB", (0, 0)))

  card_generator = get_card()

  for page in range(int(ceil(len(get_all_help_cards())/4))):
    for i, (help1, help2) in enumerate(get_all_help_cards()[page*4:page*4+4]):
      cards.append((get_help_card(help1), get_help_card(help2)))
      if i in [1, 3]:
        for _ in range(2):
          cards.append((Image.new("RGB", (0, 0)), Image.new("RGB", (0, 0))))
        if i == 3:
          for _ in range(2):
            cards.append(card_generator.__next__())
      generate_pdf(False)

  while True:
    card = card_generator.__next__()
    if card[0].size[0] == 0: break
    cards.append(card)
    generate_pdf(False)

  generate_pdf(True)



  # i = Image.open("developing/napoveda_lic.jpg")
  # i.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
  #             resolution=300, append=True)
  # i = Image.open("developing/napoveda_rub.jpg")
  # i.save("stack_overflow.pdf", save_all=True, title="Stack Overflow card game",
  #        resolution=300, append=True)

