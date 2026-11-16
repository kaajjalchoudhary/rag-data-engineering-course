"""Module 05 · Embeddings and similarity. Lesson: lessons/05_embeddings.md

A real system calls an embedding model. To keep the course offline and deterministic we use a
hashing embedder: each word is hashed into one of `dim` buckets. It captures word overlap, not
meaning, but every downstream technique (normalising, cosine, indexing, evaluation) is identical.

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m05
Compare with solutions/m05_embeddings.py after a real attempt.
"""

import hashlib
import math
import re
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "how",
    "i", "if", "in", "is", "it", "my", "of", "on", "or", "the", "to", "we", "what", "when",
    "with", "you", "your",
}


def tokenize(text: str) -> list[str]:
    """Lower-cased words of letters and digits, without STOPWORDS, with a trailing "s" removed
    from words longer than 3 letters (a crude stemmer: "refunds" -> "refund")."""
    raise NotImplementedError("Write your answer here")


def _bucket(token: str, dim: int) -> int:
    # md5 (not Python's hash()) so results are identical across runs and machines.
    return int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % dim


def embed(text: str, dim: int = 256) -> list[float]:
    """Hashing bag-of-words vector of length `dim`, L2-normalised (all zeros if no tokens)."""
    raise NotImplementedError("Write your answer here")


def l2_normalize(vec: list[float]) -> list[float]:
    """Scale to unit length so the dot product equals cosine similarity. Zero vectors stay zero."""
    raise NotImplementedError("Write your answer here")


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine of the angle between a and b; 0.0 if either has zero length."""
    raise NotImplementedError("Write your answer here")
