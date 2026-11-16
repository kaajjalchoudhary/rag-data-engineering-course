"""Module 02 · PII redaction before indexing. Lesson: lessons/02_pii_redaction.md

Your turn: replace each NotImplementedError, then run
    COURSE_TARGET=exercises pytest -k m02
Compare with solutions/m02_pii_redaction.py after a real attempt.
"""

import re
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\w)\+?\d[\d\s\-()]{5,}\d(?!\w)")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,3})?\b")


def redact_pii(text: str) -> str:
    """Replace emails, IBANs and phone numbers with [EMAIL], [IBAN] and [PHONE].

    Order matters: IBANs contain long digit runs, so they are replaced before phones.
    """
    raise NotImplementedError("Write your answer here")


def pii_report(text: str) -> dict[str, int]:
    """Count what would be redacted: {"email": n, "iban": n, "phone": n}."""
    raise NotImplementedError("Write your answer here")
