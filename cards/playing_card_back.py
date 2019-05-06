from cards.back_card import BackCard


class PlayingCardBack(BackCard):
  def __init__(self, color):
    super().__init__(87, 57, True, color)
