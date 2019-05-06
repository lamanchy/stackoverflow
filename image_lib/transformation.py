from image_lib.quality_constants import RESIZE_WAY, RESAMPLE_WAY


def rotate(img, angle, expand=True, center=None, translate=None, fillcolor=None):
  return img.rotate(angle, resample=RESAMPLE_WAY, expand=expand,
                    center=center, translate=translate, fillcolor=fillcolor)


def transform(img, size, method, data=None, fill=1, fillcolor=None):
  return img.transform(size, method, resample=RESAMPLE_WAY, data=data, fill=fill, fillcolor=fillcolor)


def resize(img, xy, box=None):
  return img.resize(xy, resample=RESIZE_WAY, box=box)
