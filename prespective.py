# To apply a perspective transformation you first have to know four points in a plane A that will be mapped
# to four points in a plane B. With those points, you can derive the homographic transform. By doing this,
# you obtain your 8 coefficients and the transformation can take place.

# The site http://xenia.media.mit.edu/~cwren/interpolator/ (mirror: WebArchive), as well as many other
# texts, describes how those coefficients can be determined. To make things easy, here is a direct
# implementation according from the mentioned link:
import random
from random import randint

import numpy
from PIL import Image, ImageColor, ImageDraw

from generate_pdf import get_card_back, mm_to_px, show, CARD_SIZE_MM, color_codes, blendify_color, get_font, \
  get_value_card_front, get_fn_card_front, RESAMPLE_WAY, RESIZE_WAY, HIGH_QUALITY, find_coefficients, box_size, \
  get_picture_card
from rules import get_rules
from values import values






for i in range(1):
  show(get_picture_card(*get_picture_cards(i)))
