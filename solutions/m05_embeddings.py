"""Module 05 · Embeddings and similarity. Lesson: lessons/05_embeddings.md

A real system calls an embedding model. To keep the course offline and deterministic we use a
hashing embedder: each word is hashed into one of `dim` buckets. It captures word overlap, not
meaning, but every downstream technique (normalising, cosine, indexing, evaluation) is identical.
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
    tokens = []
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]
        tokens.append(word)
    return tokens


def _bucket(token: str, dim: int) -> int:
    # md5 (not Python's hash()) so results are identical across runs and machines.
    return int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % dim


def embed(text: str, dim: int = 256) -> list[float]:
    """Hashing bag-of-words vector of length `dim`, L2-normalised (all zeros if no tokens)."""
    vec = [0.0] * dim
    for token in tokenize(text):
        vec[_bucket(token, dim)] += 1.0
    return l2_normalize(vec)


def l2_normalize(vec: list[float]) -> list[float]:
    """Scale to unit length so the dot product equals cosine similarity. Zero vectors stay zero."""
    norm = math.sqrt(sum(v * v for v in vec))
    return [v / norm for v in vec] if norm else list(vec)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine of the angle between a and b; 0.0 if either has zero length."""
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if not na or not nb:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)
