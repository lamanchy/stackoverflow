from cards.card_face import CardFace
from cards.colored_card import ColoredCard


class FrontCard(ColoredCard):
  def __init__(self, width, height, is_round, color):
    super().__init__(width, height, is_round, CardFace.FRONT, color)

  def get_card(self):
    card = super().get_card()
    border_color = self.blendified_color(1.5, 0)

    self.paste_centered_rectangle(card, 7, border_color)
    self.paste_centered_rectangle(card, 8, "black")

    return card
