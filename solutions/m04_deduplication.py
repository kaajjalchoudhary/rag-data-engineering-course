"""Module 04 · Deduplication: exact and near-duplicate chunks. Lesson: lessons/04_deduplication.md"""

import hashlib
import re


def content_hash(text: str) -> str:
    """SHA-256 hex digest of the text after lower-casing and collapsing whitespace,
    so formatting-only differences produce the same hash."""
    canonical = " ".join(text.lower().split())
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def dedupe_exact(chunks: list[str]) -> list[str]:
    """Keep the first occurrence of each chunk by content_hash, preserving order."""
    seen: set[str] = set()
    kept = []
    for chunk in chunks:
        h = content_hash(chunk)
        if h not in seen:
            seen.add(h)
            kept.append(chunk)
    return kept


def shingles(text: str, k: int = 3) -> set[tuple[str, ...]]:
    """Set of k-word shingles from lower-cased words (letters and digits only).
    Text with fewer than k words yields one shingle of all its words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    if len(words) < k:
        return {tuple(words)} if words else set()
    return {tuple(words[i:i + k]) for i in range(len(words) - k + 1)}


def jaccard(a: set, b: set) -> float:
    """|a ∩ b| / |a ∪ b|, and 0.0 when both are empty."""
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def near_duplicate_pairs(chunks: dict[str, str], threshold: float = 0.8) -> list[tuple[str, str, float]]:
    """All pairs of chunk ids whose shingle Jaccard similarity is >= threshold.

    Returns (id_a, id_b, similarity rounded to 3) with id_a < id_b, sorted by id_a then id_b.
    Brute force is fine for a course; at scale use MinHash + LSH to avoid comparing every pair.
    """
    ids = sorted(chunks)
    sh = {i: shingles(chunks[i]) for i in ids}
    pairs = []
    for x in range(len(ids)):
        for y in range(x + 1, len(ids)):
            s = jaccard(sh[ids[x]], sh[ids[y]])
            if s >= threshold:
                pairs.append((ids[x], ids[y], round(s, 3)))
    return pairs
