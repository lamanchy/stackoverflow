from cards.front_card import FrontCard


class HelpCard(FrontCard):
  def __init__(self, color):
    super().__init__(87, 57 * 2, False, color)
