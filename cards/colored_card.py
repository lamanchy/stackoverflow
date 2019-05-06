from cards.faced_card import FacedCard
from colors import getrgb


class ColoredCard(FacedCard):
  def __init__(self, width, height, is_round, card_face, color):
    super().__init__(width, height, is_round, card_face)
    self.color = color

  def blendified_color(self, div=1, sub=0):
    color = list(getrgb(self.color))
    for i in range(len(color)): color[i] /= div
    for i in range(len(color)): color[i] = max(color[i] - sub, 0)
    for i in range(len(color)): color[i] = int(color[i])
    return tuple(color)
