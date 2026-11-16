"""Module 08 · Hybrid search: BM25 keyword scores fused with vector scores. Lesson: lessons/08_hybrid_search.md"""

from __future__ import annotations

import math
from collections import Counter

from .m05_embeddings import tokenize


class BM25:
    """Okapi BM25 over a fixed set of documents {doc_id: text}."""

    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tokens = {doc_id: tokenize(text) for doc_id, text in docs.items()}
        self.n = len(docs)
        self.avgdl = sum(len(t) for t in self.tokens.values()) / self.n if self.n else 0.0
        self.df = Counter(term for toks in self.tokens.values() for term in set(toks))

    def idf(self, term: str) -> float:
        """BM25 idf with +1 inside the log, so it is never negative."""
        df = self.df.get(term, 0)
        return math.log((self.n - df + 0.5) / (df + 0.5) + 1)

    def score(self, query: str, doc_id: str) -> float:
        """Sum over query terms present in the doc of idf * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / avgdl)),
        where f is the term frequency in the doc and dl the doc length in tokens."""
        toks = self.tokens[doc_id]
        tf = Counter(toks)
        total = 0.0
        for term in tokenize(query):
            if term not in tf:
                continue
            f = tf[term]
            denom = f + self.k1 * (1 - self.b + self.b * len(toks) / self.avgdl)
            total += self.idf(term) * f * (self.k1 + 1) / denom
        return total

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        """Top-k (doc_id, score rounded to 4) with score > 0, best first, ties by id."""
        scored = [(d, round(self.score(query, d), 4)) for d in self.tokens]
        scored = [s for s in scored if s[1] > 0]
        scored.sort(key=lambda item: (-item[1], item[0]))
        return scored[:k]


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Fuse several ranked id lists: score(id) = sum of 1 / (k + rank), rank starting at 1.

    RRF uses only positions, so it needs no score normalisation between BM25 and cosine.
    Returns (id, score rounded to 5) best first, ties by id.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    fused = [(d, round(s, 5)) for d, s in scores.items()]
    fused.sort(key=lambda item: (-item[1], item[0]))
    return fused
