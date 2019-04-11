# To apply a perspective transformation you first have to know four points in a plane A that will be mapped
# to four points in a plane B. With those points, you can derive the homographic transform. By doing this,
# you obtain your 8 coefficients and the transformation can take place.

# The site http://xenia.media.mit.edu/~cwren/interpolator/ (mirror: WebArchive), as well as many other
# texts, describes how those coefficients can be determined. To make things easy, here is a direct
# implementation according from the mentioned link:

import numpy
import sys
from PIL import Image

from generate_pdf import get_card_back, mm_to_px, show


def find_coefficients(pa, pb):
  matrix = []
  for p1, p2 in zip(pa, pb):
    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

  A = numpy.matrix(matrix, dtype=numpy.float)
  B = numpy.array(pb).reshape(8)

  res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
  return numpy.array(res).reshape(8)


img = Image.new("RGBA", mm_to_px(200, 150), (49, 51, 53, 0))
width, height = img.size

fn_back = get_card_back("yellow")
fn_back = fn_back.rotate(90, expand=True)
img.paste(fn_back, mm_to_px(20, 20), fn_back)
value_back = get_card_back("blue")
value_back = value_back.rotate(90, expand=True)
img.paste(value_back, mm_to_px(100, 20), value_back)


def get_main_plane_coeffs(plane_size, ratio_x, ratio_y, height):
  card_z = mm_to_px(0.36)
  card_height = card_z * height
  shrink_x = (plane_size[0] - (plane_size[0]*ratio_x)) / 2
  return find_coefficients(
    [
      (shrink_x, - card_height * ratio_x),
      (plane_size[0] - shrink_x, - card_height * ratio_x),
      (plane_size[0], (plane_size[1] - card_height) * ratio_y),
      (0, (plane_size[1] - card_height) * ratio_y)
    ],
    [(0, 0), (plane_size[0], 0), (plane_size[0], plane_size[1]), (0, plane_size[1])]
  )


plane = Image.new("RGBA", mm_to_px(200, 150), (49, 51, 53, 255))
for height in range(50):
  ratio = .8
  coeffs = get_main_plane_coeffs(plane.size, ratio, ratio, height-0.5)
  transofrmed = img.transform(plane.size, Image.PERSPECTIVE, coeffs,
              Image.BICUBIC)
  # print(img.size, (width, height))
  # show(transofrmed)
  plane.paste(Image.new("RGBA", mm_to_px(200, 150), (49, 51, 53, 255)), mask=transofrmed)

  # if height > 10:
  #   show(transofrmed)
  #   break

  coeffs = get_main_plane_coeffs(plane.size, ratio, ratio, height)
  transofrmed = img.transform(plane.size, Image.PERSPECTIVE, coeffs,
              Image.BICUBIC)
  # print(img.size, (width, height))
  # show(transofrmed)
  plane.paste(transofrmed, mask=transofrmed)

show(plane)
exit(0)


img = Image.open(sys.argv[1])
width, height = img.size
m = -0.5
xshift = abs(m) * width
new_width = width + int(round(xshift))
# img = img.transform((new_width, height), Image.AFFINE,
#                     (1, m, -xshift if m > 0 else 0, 0, 1, 0), Image.BICUBIC)
# img.save(sys.argv[2])
print(new_width, width)
