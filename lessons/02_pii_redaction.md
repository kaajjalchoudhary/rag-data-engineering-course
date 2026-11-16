# 02 · PII redaction before indexing

**Exercise:** [`exercises/m02_pii_redaction.py`](../exercises/m02_pii_redaction.py)

Anything you embed can be retrieved and shown to a user, or pasted into an LLM prompt. Redact personal
data **before** chunking and embedding; removing it afterwards means re-indexing and hoping no copy
survived in a cache.

## Pattern-based redaction

```python
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
text = EMAIL.sub("[EMAIL]", text)
```

- Replace with a **typed placeholder** (`[EMAIL]`, `[PHONE]`), not an empty string. The sentence still
  reads naturally and the model knows something was there.
- **Order matters.** An IBAN contains a long digit run that a phone pattern would also match; redact the
  more specific pattern first.
- Test for **false positives** as carefully as for misses: "30 days", "14:00" and "9.95 EUR" must survive.

## Report, don't just redact

Counting what was found per document (`pii_report`) gives you monitoring: a sudden jump in emails in a
"policy" folder usually means someone exported a mailbox into the knowledge base.

## Beyond regex

Names and addresses need NER models (spaCy, Presidio). Regex is still the right first layer: fast,
explainable and easy to test. Under GDPR, also record *which* sources contain personal data so you
can honour deletion requests across the index.
