# 06 · A vector index with metadata filters

**Exercise:** [`exercises/m06_vector_index.py`](../exercises/m06_vector_index.py)

A vector index stores records of `(id, vector, metadata, text)` and answers "top k nearest to this
query vector".

## Exact vs approximate search

The course index scores every record (exact, brute force). That is fine up to tens of thousands of
vectors. Beyond that, approximate nearest neighbour (ANN) indexes such as **HNSW** (pgvector, Qdrant,
Weaviate) or **IVF** (FAISS) answer in milliseconds by visiting only part of the data, at the cost of
occasionally missing a true neighbour. Measure that loss with recall (module 09).

## Metadata filters

Real questions come with constraints: language, product line, customer tier, document access level.

```python
index.search("refund", k=5, where={"lang": "de"})
```

**Filter for access control at query time**, from the user's permissions, never by trusting the
prompt. A RAG system that retrieves a document the user may not read has leaked it, whatever the
model then says.

## Upsert and delete

Use ids as primary keys: `upsert` replaces, `delete` removes. Without deletes, a policy you withdrew
months ago keeps being retrieved and quoted.
