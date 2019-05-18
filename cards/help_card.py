from cards.card import Card
from cards.front_card import FrontCard


class HelpCard(FrontCard):
  def __init__(self, color):
    super().__init__(Card.base_width, Card.base_height * 2, False, color)
