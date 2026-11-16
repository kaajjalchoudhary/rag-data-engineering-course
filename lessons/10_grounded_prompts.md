# 10 · Grounded prompts and citations

**Exercise:** [`exercises/m10_grounded_prompts.py`](../exercises/m10_grounded_prompts.py)

The final data step is assembling what the model sees. Its job: the right context, within budget,
with sources the model can cite, and an honest "I don't know" path.

## Context selection

- Go through hits best-first and stop before the **token budget** is exceeded.
- Drop hits below a **minimum score**. Weak matches look like context and invite confident wrong
  answers.
- If nothing survives, **do not call the model**: return a fixed "not found" answer. That is cheaper and
  safer than asking the model to answer from nothing.

## Prompt structure

```
Answer the question using only the sources below. Cite sources as [n].
If the sources do not contain the answer, say you do not know.

Sources:
[1] (refund_policy#0) Customers can request a refund within 30 days ...
[2] (returns_faq#0) ...

Question: How many days do I have to request a refund?
Answer:
```

Numbered sources with chunk ids let you map `[1]` back to a document and show it to the user.

## Check the answer

Validate citations after generation: a reference like `[3]` when only two sources were sent means the
model invented a source. Log it, and treat answers without valid citations as unverified.
