# 04 · Deduplication

**Exercise:** [`exercises/m04_deduplication.py`](../exercises/m04_deduplication.py)

Duplicates waste embedding cost and, worse, fill the top-k results with the same text, pushing out the
chunk that actually answers the question.

## Exact duplicates: content hashes

Hash a canonical form (lower-cased, whitespace collapsed) with SHA-256. Equal hashes mean equal content.
The same hash is reused as the change detector in module 07.

## Near duplicates: shingles and Jaccard

A k-shingle is a run of k consecutive words. Two texts are similar when they share many shingles:

```
jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

In the course data, the first chunk of `refund_policy` and the first chunk of `returns_faq` repeat the
same sentence. That is typical of real knowledge bases: an FAQ copies policy text, then one copy is
updated and the other is not. Find these pairs and decide which source is authoritative.

## At scale

Comparing every pair is O(n²). MinHash compresses shingle sets into short signatures, and
locality-sensitive hashing (LSH) only compares candidates that collide in a bucket, which makes
near-duplicate detection practical on millions of chunks.
