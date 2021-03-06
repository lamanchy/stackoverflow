from PIL import ImageColor

color_codes = {
  "black": "#2b2b2b",
  "true_black": "#000000",
  "lighter_black": "#313335",
  "white": "rgb(212,225,240)",
  "true_white": "#FFFFFF",
  "blue": "rgb(102,180,250)",
  "violet": "rgb(169,168,255)",
  "orange": "rgb(230,142,71)",
  "yellow": "#FFC66D",
  "bright_yellow": "#A8C023",
  "green": "rgb(100,183,70)",
  "grey": "rgb(166,166,166)",
  "red": "rgb(216,69,65)",
  "cyan": "rgb(82,187,186)",
  "magenta": "rgb(194,158,211)",
}

color_regexes = [
  (r".*", "white"),  # default color
  (r"(?:\W|^)(\d+)", "blue"),
  (r"(-|\.)(?=\d)", "blue"),
  (r"(√|π|pi|inf)", "blue"),
  (
    r'(?:^|\s|\(|\[|{)(round|range|abs|max|min|floor|len|gcd|lcm|nsd|nsn|is_prime|prime|sqrt|ceil|log2|sin|int|str'
    r'|pow|float|eval|sign|isnan|input|get_all_cards|shuffle|all|enumerate'
    r'|isinf|ZeroDivisionError|ValueError|TypeError|RecursionError|Exception)(?=\(|:|\s|\)|,|$)',
    "violet"),
  (r'(?:^|\s|=)(lambda|def|if|while|and|or|else|elif|for|in|return|None|global'
   r'|is|except|try|as)(?=\W|:|\))', "orange"),
  (r'pass', "orange"),
  (r'def (\w*)', "yellow"),
  (r"'[^'\n]*'", "green"),
  (r"(?:[\s\(])\"[^\"]*\"", "green"),
  (r"(f\"[^{]*)(?:{)(?:[^:]*)(?::)(?:[^}]*)(?:})(?:[^\"]*\")", "green"),
  (r"(?:f\"[^{]*)({)(?:[^:]*)(?::)(?:[^}]*)(?:})(?:[^\"]*\")", "orange"),
  (r"(?:f\"[^{]*)(?:{)(?:[^:]*)(:)(?:[^}]*)(?:})(?:[^\"]*\")", "orange"),
  (r"(?:f\"[^{]*)(?:{)(?:[^:]*)(?::)(?:[^}]*)(})(?:[^\"]*\")", "orange"),
  (r"(?:f\"[^{]*)(?:{)(?:[^:]*)(?::)([^}]*)(?:})(?:[^\"]*\")", "green"),
  (r"(?:f\"[^{]*)(?:{)(?:[^:]*)(?::)(?:[^}]*)(?:})([^\"]*\")", "green"),
  (r'#.*', "grey"),
  (r'# TODO.*', "bright_yellow"),
  (r'①', "green"),
  (r'②', "yellow"),
  (r'③', "red"),
  (r'④', "white"),
]


def getrgb(color):
  return ImageColor.getrgb(color_codes[color])
