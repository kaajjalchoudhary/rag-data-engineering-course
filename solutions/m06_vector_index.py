"""Module 06 · A vector index with metadata filters. Lesson: lessons/06_vector_index.md"""

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
        self.records[record_id] = {
            "id": record_id,
            "text": text,
            "vector": embed(text, self.dim),
            "metadata": dict(metadata or {}),
        }

    def delete(self, record_id: str) -> None:
        """Remove a record if present (no error if missing)."""
        self.records.pop(record_id, None)

    def __len__(self) -> int:
        return len(self.records)

    def search(self, query: str, k: int = 3, where: dict | None = None) -> list[tuple[str, float]]:
        """Top-k (id, score) by dot product with the embedded query, best first.

        `where` keeps only records whose metadata matches every key/value given. Ties are broken
        by id so results are deterministic. Records with score 0 are not returned.
        """
        q = embed(query, self.dim)
        scored = []
        for rec in self.records.values():
            if where and any(rec["metadata"].get(key) != value for key, value in where.items()):
                continue
            score = sum(a * b for a, b in zip(q, rec["vector"]))
            if score > 0:
                scored.append((rec["id"], round(score, 4)))
        scored.sort(key=lambda item: (-item[1], item[0]))
        return scored[:k]
