"""Module 10 · Building grounded prompts with citations. Lesson: lessons/10_grounded_prompts.md

No model is called here: the job of the data pipeline is to hand the model the right context,
within budget, with sources it can cite, and to say "I don't know" when retrieval found nothing.

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m10
Compare with solutions/m10_grounded_prompts.py after a real attempt.
"""

from __future__ import annotations
import re
NO_CONTEXT_ANSWER = "I could not find this in the knowledge base."


def estimate_tokens(text: str) -> int:
    """Rough token count: 1 token per 4 characters, rounded up (a common rule of thumb)."""
    raise NotImplementedError("Write your answer here")


def select_context(hits: list[tuple[str, float]], chunks: dict[str, str],
                   token_budget: int, min_score: float = 0.1) -> list[str]:
    """Pick chunk ids from best-first hits until the next one would exceed token_budget.

    Hits below min_score are dropped: weak matches add noise and invite hallucination.
    """
    raise NotImplementedError("Write your answer here")


def build_prompt(question: str, context_ids: list[str], chunks: dict[str, str]) -> str:
    """Prompt with numbered sources, or "" when there is no context (so the caller can refuse)."""
    raise NotImplementedError("Write your answer here")


def check_citations(answer: str, n_sources: int) -> dict[str, list[int]]:
    """Validate an answer's [n] citations: {"valid": [...], "invalid": [...]} sorted, unique."""
    raise NotImplementedError("Write your answer here")
