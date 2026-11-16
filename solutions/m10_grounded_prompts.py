"""Module 10 · Building grounded prompts with citations. Lesson: lessons/10_grounded_prompts.md

No model is called here: the job of the data pipeline is to hand the model the right context,
within budget, with sources it can cite, and to say "I don't know" when retrieval found nothing.
"""

from __future__ import annotations

import re

NO_CONTEXT_ANSWER = "I could not find this in the knowledge base."


def estimate_tokens(text: str) -> int:
    """Rough token count: 1 token per 4 characters, rounded up (a common rule of thumb)."""
    return -(-len(text) // 4)


def select_context(hits: list[tuple[str, float]], chunks: dict[str, str],
                   token_budget: int, min_score: float = 0.1) -> list[str]:
    """Pick chunk ids from best-first hits until the next one would exceed token_budget.

    Hits below min_score are dropped: weak matches add noise and invite hallucination.
    """
    selected, used = [], 0
    for chunk_id, score in hits:
        if score < min_score:
            continue
        cost = estimate_tokens(chunks[chunk_id])
        if used + cost > token_budget:
            break
        selected.append(chunk_id)
        used += cost
    return selected


def build_prompt(question: str, context_ids: list[str], chunks: dict[str, str]) -> str:
    """Prompt with numbered sources, or "" when there is no context (so the caller can refuse)."""
    if not context_ids:
        return ""
    sources = "\n".join(f"[{n}] ({cid}) {chunks[cid]}" for n, cid in enumerate(context_ids, start=1))
    return (
        "Answer the question using only the sources below. "
        "Cite sources as [n]. If the sources do not contain the answer, say you do not know.\n\n"
        f"Sources:\n{sources}\n\nQuestion: {question}\nAnswer:"
    )


def check_citations(answer: str, n_sources: int) -> dict[str, list[int]]:
    """Validate an answer's [n] citations: {"valid": [...], "invalid": [...]} sorted, unique."""
    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer)})
    return {
        "valid": [n for n in cited if 1 <= n <= n_sources],
        "invalid": [n for n in cited if not 1 <= n <= n_sources],
    }
