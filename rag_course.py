"""Shared helpers: load the sample documents and the golden question set."""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def load_documents() -> dict[str, str]:
    """Return {doc_id: raw text} for every Markdown file in data/docs, sorted by doc_id."""
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted((DATA / "docs").glob("*.md"))}


def load_golden_questions() -> list[dict]:
    """Questions with the document that answers them, for retrieval evaluation."""
    return json.loads((DATA / "golden_questions.json").read_text(encoding="utf-8"))
