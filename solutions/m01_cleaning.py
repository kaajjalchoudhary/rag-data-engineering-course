"""Module 01 · Loading and cleaning documents. Lesson: lessons/01_cleaning.md"""

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalise raw document text before anything else touches it.

    - Unicode NFKC (turns non-breaking spaces and full-width characters into plain ones)
    - Windows and old Mac line endings to "\\n"
    - trailing spaces removed from every line
    - runs of spaces or tabs inside a line collapsed to one space
    - three or more newlines collapsed to a single blank line
    - leading and trailing whitespace of the whole text removed
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_markdown(text: str) -> str:
    """Remove Markdown syntax that adds noise to embeddings but keep the words.

    Headings lose their leading #s, **bold** and *italic* markers are removed,
    and [link text](url) becomes just "link text".
    """
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def extract_title(text: str) -> str:
    """The text of the first Markdown level-1 heading, or "" if there is none."""
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""
