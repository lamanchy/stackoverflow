import inspect
import re
from numbers import Number

from PIL import Image, ImageFont, ImageDraw, ImageColor
from PIL.Image import ANTIALIAS

from rules import get_rules, get_all_functions
from values import get_all_values

FONT = "fonts/DejaVuSansMono.ttf"

ANTIALIASING = 1  # do not set bigger that 32 :D
RESOLUTION_DPI = 100
CARD_SIZE_MM = (87, 57)

RESOLUTION_DPI *= ANTIALIASING


def do_antialiasing(img):
    return img.resize((img.size[0] // ANTIALIASING, img.size[1] // ANTIALIASING), ANTIALIAS)


def show(img):
    do_antialiasing(img).show()


# dasda

def mm_to_px(*args):
    x = args
    if len(args) == 1:
        x = args[0]
    if isinstance(x, Number):
        return int(RESOLUTION_DPI * 0.03937 * x)

    return type(x)([mm_to_px(i) for i in x])


def get_font(size):
    return ImageFont.truetype(FONT, size=size * RESOLUTION_DPI // 100)


color_codes = {
    "black": "#2b2b2b",
    "true_black": "#000000",
    "lighter_black": "#313335",
    "white": "#A9B7C6",
    "blue": "#6897BB",
    "violet": "#8888C6",
    "orange": "#CC7832",
    "yellow": "#FFC66D",
    "green": "#6A8759",
    "grey": "#808080",
    "red": "#AA4926",
}


def get_source_code(fn):
    source_code = inspect.getsource(fn)

    # remove leading and ending spaces
    source_code = source_code.strip()

    if source_code.startswith("lambda") and source_code[-1] == ',':
        source_code = source_code[:-1]

    return source_code


color_regexes = [
    (r".*", "white"),  # default color
    (r"\d", "blue"),  # default color
    (r'(?:^|\s)(round|range|abs|max|min|floor|len)', "violet"),
    (r'(?:^|\s)(lambda|def|if|while|and|or|else|elif|for|in|return)', "orange"),
    (r'def (\w*)', "yellow"),
    (r"'[^']*'", "green"),
    (r'"[^"]*"', "green"),
    (r'#\s.*', "grey"),
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
            if not re.match(r'\s', char) and char_color != color:
                char = " "
            result[color] += char

    return result


def get_round_rectangle(size=CARD_SIZE_MM, color="black", radius=10):
    rectangle = Image.new('RGBA', mm_to_px(size), (*ImageColor.getrgb(color_codes[color]), 0))
    draw = ImageDraw.Draw(rectangle)
    draw.rectangle(mm_to_px(radius // 2, 0, size[0] - (radius // 2), size[1]), fill=color_codes[color])
    draw.rectangle(mm_to_px(0, radius // 2, size[0], size[1] - (radius // 2)), fill=color_codes[color])
    draw.ellipse(mm_to_px(0, 0, radius, radius), fill=color_codes[color])
    draw.ellipse(mm_to_px(size[0] - radius, 0, size[0], radius), fill=color_codes[color])
    draw.ellipse(mm_to_px(0, size[1] - radius, radius, size[1]), fill=color_codes[color])
    draw.ellipse(mm_to_px(size[0] - radius, size[1] - radius, size[0], size[1]), fill=color_codes[color])
    return rectangle


def get_card_base():
    card = get_round_rectangle(CARD_SIZE_MM, "true_black")
    border = get_round_rectangle((CARD_SIZE_MM[0] - 6, CARD_SIZE_MM[1] - 6), "lighter_black", radius=6)
    card.paste(border, mm_to_px(3, 3), mask=border)
    background = get_round_rectangle((CARD_SIZE_MM[0] - 8, CARD_SIZE_MM[1] - 8), "black", radius=4)
    card.paste(background, mm_to_px(4, 4), mask=background)
    return card


def get_card_base_with_color(color):
    card = get_card_base()
    draw = ImageDraw.Draw(card)
    base_size = 6
    move_up = 3
    move_left = 3
    smaller_by = 0
    draw.ellipse(mm_to_px(
        move_left + smaller_by,
        CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
        base_size + move_left - smaller_by,
        CARD_SIZE_MM[1] - move_up - smaller_by
    ), fill=color_codes["black"])
    smaller_by = 1
    draw.ellipse(mm_to_px(
        move_left + smaller_by,
        CARD_SIZE_MM[1] - base_size - move_up + smaller_by,
        base_size + move_left - smaller_by,
        CARD_SIZE_MM[1] - move_up - smaller_by
    ), fill=color_codes[color])

    return card


def get_source_code_position_n_size(source_code, draw):
    # width is exactly half the height

    min_font_size = 1
    max_font_size = 25
    available_size = mm_to_px(CARD_SIZE_MM[0] - 30, CARD_SIZE_MM[1] - 30)

    while True:
        size = draw.textsize(source_code, get_font(min_font_size))

        if size[0] >= available_size[0] or size[1] >= available_size[1] or min_font_size == max_font_size:
            return min_font_size - 1

        min_font_size += 1


def get_fn_card_front(fn, color):
    source_code = get_source_code(fn)
    colors = get_source_code_coloring(source_code)

    card = get_card_base_with_color(color)
    base = Image.new("RGBA", mm_to_px(CARD_SIZE_MM), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    sc_size = get_source_code_position_n_size(source_code, draw)
    font = get_font(sc_size)
    W, H = mm_to_px(CARD_SIZE_MM)
    w, h = draw.textsize(source_code, font)

    for color in colors:
        draw.text((mm_to_px(10), (H - h) // 2 - mm_to_px(2)), colors[color], font=font, fill=color_codes[color])

    card.paste(base, mask=base)

    return card


def get_value_card_front(value, color):
    value = "{0:.5f}".format(value).rstrip('0').rstrip('.')
    card = get_card_base_with_color(color)
    draw = ImageDraw.Draw(card)
    font = get_font(30)
    W, H = mm_to_px(CARD_SIZE_MM)
    w, h = draw.textsize(value, font)

    draw.text(((W - w) // 2, (H - h) // 2), value, font=font, fill=color_codes["blue"])

    return card



def get_card_back(color):
    card = get_card_base()
    draw = ImageDraw.Draw(card)
    text = "Stack Overflow"
    W, H = mm_to_px(CARD_SIZE_MM)
    font = get_font(15)
    w, h = draw.textsize(text, font)
    draw.text(((W - w) // 2, (H - h) // 2), text, font=font, fill=color_codes[color])
    return card


def get_fn_card(fn, color):
    return get_fn_card_front(fn, color), get_card_back("yellow")


def get_value_card(value, color):
    return get_value_card_front(value, color), get_card_back("blue")


if __name__ == "__main__":
    fn = get_rules()["yellow"][-1]

    cards = [get_fn_card(fn, c) for fn, c in get_all_functions()]
    cards += [get_value_card(v, c) for v, c in get_all_values()]

    front_canvas = back_canvas = None # deklarace
    base_point = int(mm_to_px(210) / 2 - mm_to_px(CARD_SIZE_MM[0])),\
                 int(mm_to_px(297) / 2 - 2.5 * mm_to_px(CARD_SIZE_MM[1]) - mm_to_px(2.5))
    pages = []
    for i, card in enumerate(cards):
        i_mod = i % 10
        if i_mod == 0:
            front_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))
            back_canvas = Image.new("RGB", mm_to_px(210, 297), (255, 255, 255))

        offset_x = mm_to_px(CARD_SIZE_MM[0] + 1) if i % 2 == 1 else 0
        offset_y = mm_to_px(CARD_SIZE_MM[1] + 1) * (i_mod - (i % 2)) // 2

        front_canvas.paste(card[0], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[0])
        offset_x = mm_to_px(CARD_SIZE_MM[0] + 1) if i % 2 == 0 else 0
        back_canvas.paste(card[1], (base_point[0] + offset_x, base_point[1] + offset_y), mask=card[1])

        if i_mod == 9 or i + 1 == len(cards):
            pages.append(front_canvas)
            pages.append(back_canvas)

    pages[0].save("stack_overflow.pdf", save_all=True, append_images=pages[1:], title="Stack Overflow card game", resolution=RESOLUTION_DPI)

    exit(0)

    for fn, c in get_all_functions():
        show(get_fn_card_front(fn, c))
        break
