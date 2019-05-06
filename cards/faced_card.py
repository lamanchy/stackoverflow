from cards.card import Card
from cards.card_face import CardFace


class FacedCard(Card):
  def __init__(self, width, height, is_round, card_face):
    super().__init__(width, height, is_round)
    assert isinstance(card_face, CardFace)
    self.card_face = card_face

  def is_front(self):
    return self.card_face == CardFace.FRONT
