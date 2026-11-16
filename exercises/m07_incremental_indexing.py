"""Module 07 · Incremental indexing: only re-embed what changed. Lesson: lessons/07_incremental_indexing.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m07
Compare with solutions/m07_incremental_indexing.py after a real attempt.
"""

from __future__ import annotations
from .m03_chunking import structure_aware_chunks
from .m04_deduplication import content_hash
from .m06_vector_index import VectorIndex


def chunk_document(doc_id: str, text: str, max_chars: int = 300) -> dict[str, str]:
    """{chunk_id: chunk_text} with ids "<doc_id>#<n>" numbered from 0."""
    raise NotImplementedError("Write your answer here")


def plan_sync(current: dict[str, str], indexed_hashes: dict[str, str]) -> dict[str, list[str]]:
    """Compare chunks that should exist now with the content hashes already in the index.

    current:        {chunk_id: text} produced from today's documents
    indexed_hashes: {chunk_id: content_hash} of what the index holds

    Returns sorted id lists: {"add": new ids, "update": ids whose hash changed,
    "delete": ids no longer present, "unchanged": ids with the same hash}.
    """
    raise NotImplementedError("Write your answer here")


def apply_sync(index: VectorIndex, current: dict[str, str], indexed_hashes: dict[str, str]) -> dict[str, int]:
    """Apply plan_sync to the index and to indexed_hashes (both modified in place).

    Only added and updated chunks are embedded. Returns how many ids fell in each bucket.
    """
    raise NotImplementedError("Write your answer here")
