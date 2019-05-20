from cards.text_help_card import TextHelpCard
from cards.title_help_card import TitleHelpCard
from language import section_translator

translate = section_translator("red_tutorial")

red_tutorial = [
  TitleHelpCard(translate("title_title"), translate("title_subtitle"), "red"),
]

for i in range(1, 9):
  red_tutorial.append(TextHelpCard("red", "", translate(f"page{i}")))

for card in red_tutorial:
  card.is_upside_down = True
  card.should_resize = True
