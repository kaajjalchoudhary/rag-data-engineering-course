"""Module 06 · A vector index with metadata filters. Lesson: lessons/06_vector_index.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m06
Compare with solutions/m06_vector_index.py after a real attempt.
"""

from __future__ import annotations
from .m05_embeddings import embed


class VectorIndex:
    """Brute-force in-memory vector index.

    Each record: id, text, vector (unit length) and a metadata dict. Exact search over every
    record is what FAISS 'Flat' or pgvector without an index does; ANN indexes (HNSW, IVF)
    trade a little recall for speed on millions of vectors.
    """

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.records: dict[str, dict] = {}

    def upsert(self, record_id: str, text: str, metadata: dict | None = None) -> None:
        """Insert or replace a record, embedding its text."""
        raise NotImplementedError("Write your answer here")

    def delete(self, record_id: str) -> None:
        """Remove a record if present (no error if missing)."""
        raise NotImplementedError("Write your answer here")

    def __len__(self) -> int:
        return len(self.records)

    def search(self, query: str, k: int = 3, where: dict | None = None) -> list[tuple[str, float]]:
        """Top-k (id, score) by dot product with the embedded query, best first.

        `where` keeps only records whose metadata matches every key/value given. Ties are broken
        by id so results are deterministic. Records with score 0 are not returned.
        """
        raise NotImplementedError("Write your answer here")
