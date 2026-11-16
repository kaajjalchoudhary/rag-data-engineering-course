"""Module 03 · Chunking. Lesson: lessons/03_chunking.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m03
Compare with solutions/m03_chunking.py after a real attempt.
"""

import re


def fixed_size_chunks(text: str, size: int, overlap: int) -> list[str]:
    """Split text into windows of `size` characters, each starting `size - overlap` after the last.

    The last chunk may be shorter. Raises ValueError unless 0 <= overlap < size.
    """
    raise NotImplementedError("Write your answer here")


def split_sentences(paragraph: str) -> list[str]:
    """Split on ., ! or ? followed by whitespace. Keeps the punctuation."""
    raise NotImplementedError("Write your answer here")


def structure_aware_chunks(text: str, max_chars: int) -> list[str]:
    """Pack whole paragraphs (separated by a blank line) into chunks of at most max_chars.

    A paragraph longer than max_chars is split into sentences and those are packed instead.
    Parts inside a chunk are joined with a single space. Never cuts a sentence in half
    (a single sentence longer than max_chars becomes its own chunk).
    """
    raise NotImplementedError("Write your answer here")
