"""Module 03 · Chunking. Lesson: lessons/03_chunking.md"""

import re


def fixed_size_chunks(text: str, size: int, overlap: int) -> list[str]:
    """Split text into windows of `size` characters, each starting `size - overlap` after the last.

    The last chunk may be shorter. Raises ValueError unless 0 <= overlap < size.
    """
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    step = size - overlap
    chunks = []
    for start in range(0, len(text), step):
        chunks.append(text[start:start + size])
        if start + size >= len(text):
            break
    return chunks


def split_sentences(paragraph: str) -> list[str]:
    """Split on ., ! or ? followed by whitespace. Keeps the punctuation."""
    parts = re.split(r"(?<=[.!?])\s+", paragraph.strip())
    return [p for p in parts if p]


def structure_aware_chunks(text: str, max_chars: int) -> list[str]:
    """Pack whole paragraphs (separated by a blank line) into chunks of at most max_chars.

    A paragraph longer than max_chars is split into sentences and those are packed instead.
    Parts inside a chunk are joined with a single space. Never cuts a sentence in half
    (a single sentence longer than max_chars becomes its own chunk).
    """
    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text.strip()):
        paragraph = " ".join(paragraph.split())
        if not paragraph:
            continue
        units.extend([paragraph] if len(paragraph) <= max_chars else split_sentences(paragraph))

    chunks: list[str] = []
    current = ""
    for unit in units:
        candidate = f"{current} {unit}" if current else unit
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = unit
    if current:
        chunks.append(current)
    return chunks
