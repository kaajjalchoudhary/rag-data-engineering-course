"""Module 07 · Incremental indexing: only re-embed what changed. Lesson: lessons/07_incremental_indexing.md"""

from __future__ import annotations

from .m03_chunking import structure_aware_chunks
from .m04_deduplication import content_hash
from .m06_vector_index import VectorIndex


def chunk_document(doc_id: str, text: str, max_chars: int = 300) -> dict[str, str]:
    """{chunk_id: chunk_text} with ids "<doc_id>#<n>" numbered from 0."""
    return {f"{doc_id}#{i}": chunk for i, chunk in enumerate(structure_aware_chunks(text, max_chars))}


def plan_sync(current: dict[str, str], indexed_hashes: dict[str, str]) -> dict[str, list[str]]:
    """Compare chunks that should exist now with the content hashes already in the index.

    current:        {chunk_id: text} produced from today's documents
    indexed_hashes: {chunk_id: content_hash} of what the index holds

    Returns sorted id lists: {"add": new ids, "update": ids whose hash changed,
    "delete": ids no longer present, "unchanged": ids with the same hash}.
    """
    plan = {"add": [], "update": [], "delete": [], "unchanged": []}
    for chunk_id, text in current.items():
        if chunk_id not in indexed_hashes:
            plan["add"].append(chunk_id)
        elif indexed_hashes[chunk_id] != content_hash(text):
            plan["update"].append(chunk_id)
        else:
            plan["unchanged"].append(chunk_id)
    plan["delete"] = [i for i in indexed_hashes if i not in current]
    return {key: sorted(ids) for key, ids in plan.items()}


def apply_sync(index: VectorIndex, current: dict[str, str], indexed_hashes: dict[str, str]) -> dict[str, int]:
    """Apply plan_sync to the index and to indexed_hashes (both modified in place).

    Only added and updated chunks are embedded. Returns how many ids fell in each bucket.
    """
    plan = plan_sync(current, indexed_hashes)
    for chunk_id in plan["add"] + plan["update"]:
        index.upsert(chunk_id, current[chunk_id], {"doc_id": chunk_id.split("#")[0]})
        indexed_hashes[chunk_id] = content_hash(current[chunk_id])
    for chunk_id in plan["delete"]:
        index.delete(chunk_id)
        del indexed_hashes[chunk_id]
    return {key: len(ids) for key, ids in plan.items()}
