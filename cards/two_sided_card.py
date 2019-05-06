from typing import Tuple

from cards.card import Card


class TwoSidedCard(Card):
  def __init__(self, front: Card, back: Card):
    assert front.width == back.width
    assert front.height == back.height
    assert front.is_round == back.is_round

    super().__init__(front.width, front.height, front.is_round)

    self.front = front
    self.back = back

  def get_card(self) -> Tuple[Card, Card]:
    return self.front.get_card(), self.back.get_card()

  @staticmethod
  def empty_card():
    return TwoSidedCard(Card.empty_card(), Card.empty_card())
