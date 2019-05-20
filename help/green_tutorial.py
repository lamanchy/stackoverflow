from cards.picture_help_card import PictureHelpCard
from cards.text_help_card import TextHelpCard
from cards.title_help_card import TitleHelpCard
from help.picture_generation import get_first_image, get_play, get_first_chain_image, get_second_chain_image
from language import section_translator

translate = section_translator("green_tutorial")

green_tutorial = [
  TitleHelpCard(translate("title_title"), translate("title_subtitle"), "green"),
  TextHelpCard("green", translate("page1_title"), translate("page1_text")),
]

pictures = [
  lambda: get_first_image(),
  lambda: get_play(
    fns_count=8,
    values_count=13,
    input_value_index=None,
    output_value_index=7,
    used_fn_indexes=[],
    front_hand_count=4,
    right_hand_count=4
  ),
  lambda: get_play(
    fns_count=8,
    values_count=12,
    input_value_index=3,
    output_value_index=7,
    used_fn_indexes=[],
    front_hand_count=4,
    right_hand_count=4
  ),
  lambda: get_play(
    fns_count=8,
    values_count=12,
    input_value_index=3,
    output_value_index=7,
    used_fn_indexes=[],
    front_hand_count=3,
    right_hand_count=2,
    front_played_count=1,
    right_played_count=2,
  ),
  lambda: get_first_chain_image(),
  lambda: get_second_chain_image(),
  lambda: get_play(
    fns_count=8,
    values_count=12,
    input_value_index=3,
    output_value_index=7,
    used_fn_indexes=[5, 2, 7],
    front_hand_count=3,
    right_hand_count=2,
  ),
  lambda: get_play(
    fns_count=6,
    values_count=12,
    input_value_index=3,
    output_value_index=7,
    used_fn_indexes=[5, 2, 7],
    front_hand_count=4,
    right_hand_count=3,
  ),
  lambda: get_play(
    fns_count=6,
    values_count=6,
    input_value_index=8,
    output_value_index=7,
    used_fn_indexes=[5, 2, 7, 4, 8, 9, 11, 6],
    front_hand_count=2,
    right_hand_count=0,
  ),
]

for i, picture in enumerate(pictures):
  i += 2
  green_tutorial.append(PictureHelpCard("green", translate(f"page{i}_title"), translate(f"page{i}_text"), picture))
  green_tutorial[-1].id = i
