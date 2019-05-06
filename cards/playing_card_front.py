from cards.front_card import FrontCard


class PlayingCardFront(FrontCard):
  def __init__(self, color):
    super().__init__(87, 57, True, color)
