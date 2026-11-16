"""Module 01 · Loading and cleaning documents. Lesson: lessons/01_cleaning.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m01
Compare with solutions/m01_cleaning.py after a real attempt.
"""

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalise raw document text before anything else touches it.

    - Unicode NFKC (turns non-breaking spaces and full-width characters into plain ones)
    - Windows and old Mac line endings to "\n"
    - trailing spaces removed from every line
    - runs of spaces or tabs inside a line collapsed to one space
    - three or more newlines collapsed to a single blank line
    - leading and trailing whitespace of the whole text removed
    """
    raise NotImplementedError("Write your answer here")


def strip_markdown(text: str) -> str:
    """Remove Markdown syntax that adds noise to embeddings but keep the words.

    Headings lose their leading #s, **bold** and *italic* markers are removed,
    and [link text](url) becomes just "link text".
    """
    raise NotImplementedError("Write your answer here")


def extract_title(text: str) -> str:
    """The text of the first Markdown level-1 heading, or "" if there is none."""
    raise NotImplementedError("Write your answer here")
