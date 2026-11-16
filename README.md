# RAG Data Engineering Course

[![CI](https://github.com/kaajjalchoudhary/rag-data-engineering-course/actions/workflows/ci.yml/badge.svg)](https://github.com/kaajjalchoudhary/rag-data-engineering-course/actions/workflows/ci.yml)

A hands-on course on the data side of retrieval-augmented generation: how documents become a clean,
deduplicated, PII-safe, incrementally updated index, and how to prove retrieval works. You build every
piece yourself in plain Python, with automated tests that check each step.

Created and taught by **Kajal Choudhary**, AI & Data Engineer with 9+ years of data work in banking,
retail and e-commerce, who builds RAG solutions and AI agents over enterprise data.

## Why the data side

Most RAG problems are data problems: the right passage was never indexed, was split in half, was
buried under duplicates, or an outdated copy was retrieved instead. This course focuses on the
engineering that prevents those failures.

## Who it is for

- Data engineers moving into AI and LLM work
- ML and backend engineers building their first production RAG system
- Anyone preparing for AI data engineering interviews

Requires basic Python. **No API keys, no GPU and no downloads**: everything runs offline in seconds.

## Curriculum

| # | Module | You will build | Lesson | Exercise |
|---|---|---|---|---|
| 01 | Cleaning | Unicode and whitespace normalisation, Markdown stripping | [lesson](lessons/01_cleaning.md) | [exercise](exercises/m01_cleaning.py) |
| 02 | PII redaction | Email, phone and IBAN redaction with a PII report | [lesson](lessons/02_pii_redaction.md) | [exercise](exercises/m02_pii_redaction.py) |
| 03 | Chunking | Fixed windows with overlap and paragraph/sentence-aware chunks | [lesson](lessons/03_chunking.md) | [exercise](exercises/m03_chunking.py) |
| 04 | Deduplication | Content hashes, shingles, Jaccard near-duplicate detection | [lesson](lessons/04_deduplication.md) | [exercise](exercises/m04_deduplication.py) |
| 05 | Embeddings | Tokenising, a deterministic embedder, normalisation, cosine | [lesson](lessons/05_embeddings.md) | [exercise](exercises/m05_embeddings.py) |
| 06 | Vector index | Upsert, delete, top-k search with metadata filters | [lesson](lessons/06_vector_index.md) | [exercise](exercises/m06_vector_index.py) |
| 07 | Incremental indexing | A sync plan: add, update, delete, skip unchanged | [lesson](lessons/07_incremental_indexing.md) | [exercise](exercises/m07_incremental_indexing.py) |
| 08 | Hybrid search | BM25 from scratch and reciprocal rank fusion | [lesson](lessons/08_hybrid_search.md) | [exercise](exercises/m08_hybrid_search.py) |
| 09 | Retrieval evaluation | recall@k, MRR and hit rate on a golden set | [lesson](lessons/09_retrieval_evaluation.md) | [exercise](exercises/m09_retrieval_evaluation.py) |
| 10 | Grounded prompts | Token budgets, score thresholds, numbered citations, citation checks | [lesson](lessons/10_grounded_prompts.md) | [exercise](exercises/m10_grounded_prompts.py) |

**Interview preparation:** [RAG interview questions](interview/rag_interview_questions.md), each with a worked answer.

Modules build on each other: module 06 uses your embedder from 05, and 07 uses your chunker, hashing
and index. Work through them in order.

## The data

`data/docs/` holds a small online shop knowledge base: refund policy, returns FAQ, shipping, warranty,
account security and support contacts. It contains the problems real knowledge bases have: personal
data in the support page and a returns FAQ that copies text from the refund policy.
`data/golden_questions.json` pairs eight questions with the document that answers them.

## Getting started

```bash
git clone https://github.com/kaajjalchoudhary/rag-data-engineering-course.git
cd rag-data-engineering-course
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## How to work through a module

1. Read the lesson in `lessons/`.
2. Replace each `NotImplementedError` in the matching `exercises/` file.
3. Check your work:

   ```bash
   COURSE_TARGET=exercises pytest -k m03    # one module
   COURSE_TARGET=exercises pytest           # everything you have attempted
   ```

   Questions you have not attempted are skipped, not failed.
4. Compare with `solutions/` after a genuine attempt.

## Related

- [rag-ingestion-pipeline](https://github.com/kaajjalchoudhary/rag-ingestion-pipeline): the same ideas as an installable pipeline
- [pyspark-sql-course](https://github.com/kaajjalchoudhary/pyspark-sql-course): PySpark and SQL for data engineers

## Learn with me

I offer 1:1 and small-group sessions on RAG data engineering, PySpark and SQL: working through these
courses, reviewing your pipeline code and preparing for interviews. Get in touch on
[LinkedIn](https://www.linkedin.com/in/kaajal-choudhary).

## License

MIT
