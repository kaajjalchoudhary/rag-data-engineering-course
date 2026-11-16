# 05 · Embeddings and similarity

**Exercise:** [`exercises/m05_embeddings.py`](../exercises/m05_embeddings.py)

An embedding model maps text to a vector so that similar meanings land close together. Retrieval then
becomes "find the vectors closest to the question's vector".

## Why this course uses a hashing embedder

Real models (OpenAI, Cohere, sentence-transformers) need network access or large downloads. The
hashing embedder here (each word hashed into one of 256 buckets) runs offline and is deterministic, so
tests are exact. It only captures **word overlap**, not meaning ("refund" and "money back" do not
match), which is exactly why module 08 matters.

Swapping in a real model changes one function. Everything else stays the same.

## Cosine similarity and normalisation

```
cosine(a, b) = a · b / (|a| |b|)
```

If every vector is **L2-normalised** (length 1), cosine is just the dot product: cheaper, and what most
vector databases expect.

## Practical rules

- Embed queries and documents with the **same model and preprocessing**.
- Store the **model name and version** with every vector. Changing models means re-embedding everything;
  mixing vectors from two models silently ruins results.
- Cache embeddings by `(content_hash, model)` so unchanged chunks are never paid for twice.
