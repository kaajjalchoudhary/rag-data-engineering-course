"""Module 09 · Evaluating retrieval with a golden question set. Lesson: lessons/09_retrieval_evaluation.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m09
Compare with solutions/m09_retrieval_evaluation.py after a real attempt.
"""

from __future__ import annotations
from typing import Callable


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """Share of relevant ids found in the first k retrieved (0.0 if nothing is relevant)."""
    raise NotImplementedError("Write your answer here")


def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    """1 / position of the first relevant id (positions start at 1), 0.0 if none is found."""
    raise NotImplementedError("Write your answer here")


def evaluate(search: Callable[[str], list[str]], golden: list[dict], k: int = 3) -> dict[str, float]:
    """Run every golden question through `search` (question -> ranked doc ids).

    Returns {"recall_at_k": mean, "mrr": mean, "hit_rate": share with recall > 0}, rounded to 3.
    """
    raise NotImplementedError("Write your answer here")
