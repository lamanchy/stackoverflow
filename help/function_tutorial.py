from cards.text_help_card import TextHelpCard

# 27 lines max
from cards.title_help_card import TitleHelpCard
from language import section_translator

translate = section_translator("function_tutorial")

function_tutorial = [
  TitleHelpCard(translate("title_title"), translate("title_subtitle"), "green"),
]

colors = [
  "green",
  "green",
  "green",
  "green",
  "yellow",
  "yellow",
  "yellow",
  "red",
  "red",
  "red",
  "grey",
]

for i, color in enumerate(colors):
  i += 1
  function_tutorial.append(TextHelpCard(color, translate(f"page{i}_title"), translate(f"page{i}_text")))
