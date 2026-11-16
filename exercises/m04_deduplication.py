"""Module 04 · Deduplication: exact and near-duplicate chunks. Lesson: lessons/04_deduplication.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m04
Compare with solutions/m04_deduplication.py after a real attempt.
"""

import hashlib
import re


def content_hash(text: str) -> str:
    """SHA-256 hex digest of the text after lower-casing and collapsing whitespace,
    so formatting-only differences produce the same hash."""
    raise NotImplementedError("Write your answer here")


def dedupe_exact(chunks: list[str]) -> list[str]:
    """Keep the first occurrence of each chunk by content_hash, preserving order."""
    raise NotImplementedError("Write your answer here")


def shingles(text: str, k: int = 3) -> set[tuple[str, ...]]:
    """Set of k-word shingles from lower-cased words (letters and digits only).
    Text with fewer than k words yields one shingle of all its words."""
    raise NotImplementedError("Write your answer here")


def jaccard(a: set, b: set) -> float:
    """|a ∩ b| / |a ∪ b|, and 0.0 when both are empty."""
    raise NotImplementedError("Write your answer here")


def near_duplicate_pairs(chunks: dict[str, str], threshold: float = 0.8) -> list[tuple[str, str, float]]:
    """All pairs of chunk ids whose shingle Jaccard similarity is >= threshold.

    Returns (id_a, id_b, similarity rounded to 3) with id_a < id_b, sorted by id_a then id_b.
    Brute force is fine for a course; at scale use MinHash + LSH to avoid comparing every pair.
    """
    raise NotImplementedError("Write your answer here")
