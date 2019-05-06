from PIL import Image

from image_lib.quality_constants import ANTIALIASING
from image_lib.transformation import resize


def apply_texture(image, texture):
  texture = Image.open(texture)
  texture = resize(texture, (texture.size[0] * ANTIALIASING, texture.size[1] * ANTIALIASING))
  texture = texture.point(lambda p: p * 2)
  for x in range(0, image.size[0], texture.size[0]):
    for y in range(0, image.size[1], texture.size[1]):
      image.paste(texture, (x, y), mask=image.crop((x, y, x + texture.size[0], y + texture.size[1])))
