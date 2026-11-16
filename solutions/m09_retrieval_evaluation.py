"""Module 09 · Evaluating retrieval with a golden question set. Lesson: lessons/09_retrieval_evaluation.md"""

from __future__ import annotations

from typing import Callable


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Share of relevant ids found in the first k retrieved (0.0 if nothing is relevant)."""
    if not relevant:
        return 0.0
    return len(set(retrieved[:k]) & relevant) / len(relevant)


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    """1 / position of the first relevant id (positions start at 1), 0.0 if none is found."""
    for position, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            return 1.0 / position
    return 0.0


def evaluate(search: Callable[[str], list[str]], golden: list[dict], k: int = 3) -> dict[str, float]:
    """Run every golden question through `search` (question -> ranked doc ids).

    Returns {"recall_at_k": mean, "mrr": mean, "hit_rate": share with recall > 0}, rounded to 3.
    """
    recalls, rrs = [], []
    for item in golden:
        ranked = search(item["question"])
        relevant = {item["relevant_doc"]}
        recalls.append(recall_at_k(ranked, relevant, k))
        rrs.append(reciprocal_rank(ranked, relevant))
    n = len(golden)
    return {
        "recall_at_k": round(sum(recalls) / n, 3),
        "mrr": round(sum(rrs) / n, 3),
        "hit_rate": round(sum(1 for r in recalls if r > 0) / n, 3),
    }
