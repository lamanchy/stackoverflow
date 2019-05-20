import os

from jproperties import Properties

LANGUAGES = ["en", "cz"]
LANGUAGE = LANGUAGES[0]


def set_language(language):
  if language not in LANGUAGES:
    raise ValueError(f"Language {language} unknown, use one of {LANGUAGES}")
  global LANGUAGE
  LANGUAGE = language


def translate(section, key):
  p = Properties()
  with open(f"translations/{section}_{LANGUAGE}.properties", encoding="utf-8") as f:
    text = f.read()
    text = text.replace("=\\\n", "=")
    text = text.replace("\\\n", "\\n\\\n")
    lines = text.split("\n")
    for i, line in enumerate(lines):
      line = line.rstrip()
      spaces = len(line) - len(line.strip())
      line = "_" * spaces + line[spaces:]
      lines[i] = line
    text = "\n".join(lines)

    with open("tmp", "w", encoding="utf-8") as tmp:
      tmp.write(text)

    with open("tmp", "rb") as tmp:
      p.load(tmp, "utf-8")

    os.remove("tmp")

    data = p[key].data
    lines = data.split("\n")
    for l, line in enumerate(lines):
      for i, c in enumerate(line):
        if c != "_":
          break
        line = line[:i] + " " + line[i + 1:]
      lines[l] = line

    return "\n".join(lines)


def section_translator(section):
  return lambda name: translate(section, name)
