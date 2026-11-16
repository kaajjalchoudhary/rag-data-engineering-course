# 07 · Incremental indexing

**Exercise:** [`exercises/m07_incremental_indexing.py`](../exercises/m07_incremental_indexing.py)

Most RAG demos rebuild the whole index on every run. With real document volumes and paid embedding
APIs that is slow, expensive and risky. Treat the index like any other table and **sync** it.

## The sync plan

Compare what should exist now (`chunk_id → text`) with what the index holds (`chunk_id → content_hash`):

| Case | Action |
|---|---|
| id is new | **add**: embed and insert |
| id exists, hash differs | **update**: re-embed and replace |
| id exists, hash equal | **unchanged**: do nothing |
| id is in the index but not in the source | **delete** |

## Properties worth testing

- Running sync twice in a row changes nothing (**idempotent**).
- Editing one paragraph re-embeds one chunk.
- Deleting a document removes all its chunks.

The tests for this module check exactly these, the same guarantees as the companion project
[rag-ingestion-pipeline](https://github.com/kaajjalchoudhary/rag-ingestion-pipeline).

## A caveat on ids

Ids like `doc#3` shift when a paragraph is inserted near the top, turning one edit into many updates.
Content-addressed ids (the chunk hash) avoid that; then "update" becomes "add new + delete old".
