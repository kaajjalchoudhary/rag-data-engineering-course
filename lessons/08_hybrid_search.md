# 08 · Hybrid search

**Exercise:** [`exercises/m08_hybrid_search.py`](../exercises/m08_hybrid_search.py)

Vector search finds paraphrases; keyword search finds exact terms: product codes, error numbers,
names, "IFRS-9". Production RAG systems usually combine both.

## BM25

BM25 scores a document higher when it contains rare query terms (high **idf**), several times (term
frequency, with diminishing returns via `k1`), and is not unusually long (length normalisation via `b`).

```
score = Σ idf(t) · f·(k1+1) / (f + k1·(1 − b + b·dl/avgdl))
```

## Reciprocal rank fusion

BM25 scores and cosine scores live on different scales, so adding them is meaningless. RRF uses only
**positions**:

```
rrf(d) = Σ 1 / (k + rank_i(d))      k = 60 by convention
```

A document ranked well by both lists rises to the top; one ranked well by only one list still appears.

## When to add more

- A **re-ranker** (cross-encoder) re-scores the top 20 to 50 fused results for precision.
- **Query rewriting** expands abbreviations or splits multi-part questions before retrieval.

Add each only if the evaluation in module 09 shows it helps.
