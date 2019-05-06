import functools

from PIL import ImageFont

from image_lib.quality_constants import ANTIALIASING, RESOLUTION_DPI

FONT = "fonts/DejaVuSansMono.ttf"


@functools.lru_cache(None)
def get_font(size, font=FONT):
  return ImageFont.truetype(font, size=int(size * RESOLUTION_DPI * ANTIALIASING / 100))
