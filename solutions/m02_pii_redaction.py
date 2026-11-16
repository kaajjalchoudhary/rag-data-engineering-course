"""Module 02 · PII redaction before indexing. Lesson: lessons/02_pii_redaction.md"""

import re

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
# International or local phone numbers with at least 7 digits, allowing spaces, dashes and brackets.
PHONE = re.compile(r"(?<!\w)\+?\d[\d\s\-()]{5,}\d(?!\w)")
IBAN = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,3})?\b")


def redact_pii(text: str) -> str:
    """Replace emails, IBANs and phone numbers with [EMAIL], [IBAN] and [PHONE].

    Order matters: IBANs contain long digit runs, so they are replaced before phones.
    """
    text = EMAIL.sub("[EMAIL]", text)
    text = IBAN.sub("[IBAN]", text)
    text = PHONE.sub("[PHONE]", text)
    return text


def pii_report(text: str) -> dict[str, int]:
    """Count what would be redacted: {"email": n, "iban": n, "phone": n}."""
    after_email = EMAIL.sub("", text)
    after_iban = IBAN.sub("", after_email)
    return {
        "email": len(EMAIL.findall(text)),
        "iban": len(IBAN.findall(after_email)),
        "phone": len(PHONE.findall(after_iban)),
    }
