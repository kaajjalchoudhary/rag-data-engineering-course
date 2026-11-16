# RAG and AI data engineering interview questions

Questions asked in interviews for data and ML engineers working on retrieval-augmented generation,
with worked answers. Try each one before opening the answer.

---

### 1. Walk through a RAG ingestion pipeline end to end.

<details><summary>Answer</summary>

Extract text from sources → clean and normalise → redact PII → chunk with stable ids → deduplicate →
embed (cached by content hash and model) → upsert into a vector index with metadata → delete what
disappeared from the source. At query time: embed the question → retrieve (vector, keyword or hybrid)
with access filters → optionally re-rank → assemble a prompt within a token budget → generate → validate
citations. Evaluate retrieval separately with a golden set.
</details>

### 2. How do you choose a chunk size?

<details><summary>Answer</summary>

Start with structure-aware chunks of roughly 200 to 500 tokens, prefixed with the document title, then
measure recall@k and MRR on a golden set for a few sizes. Smaller chunks are more precise but lose
context; larger ones dilute the embedding and cost more prompt tokens.
</details>

### 3. How do you avoid re-embedding everything on every run?

<details><summary>Answer</summary>

Hash each chunk's normalised content and store the hash with its id. On each run compare: new ids are
added, changed hashes are re-embedded, missing ids are deleted, the rest is skipped. Cache embeddings by
`(content_hash, model_version)` as well. Test that a second run is a no-op.
</details>

### 4. What happens when you change the embedding model?

<details><summary>Answer</summary>

Vectors from different models are not comparable, so the whole corpus must be re-embedded. Build a new
index (or a new column) in parallel, evaluate it on the golden set, then switch reads over. Store the
model name and version with every vector so mixing is detectable.
</details>

### 5. Vector search vs keyword search: when does each fail?

<details><summary>Answer</summary>

Vector search misses exact identifiers (SKU codes, error numbers, rare names) and can return
topically similar but wrong passages. Keyword search misses paraphrases and synonyms. Hybrid search with
reciprocal rank fusion combines both without needing to normalise their scores.
</details>

### 6. How do you evaluate a RAG system?

<details><summary>Answer</summary>

Separately: **retrieval** (recall@k, MRR, hit rate against a golden set) and **generation** (faithfulness
to the retrieved context, answer correctness, citation validity), using human review or an LLM judge
calibrated against human labels. Run retrieval evaluation in CI; track production signals such as
"no answer found" rate and user feedback.
</details>

### 7. How do you handle access control in RAG?

<details><summary>Answer</summary>

Store access attributes (tenant, group, classification) as metadata on every chunk and apply them as
filters inside the retrieval query, derived from the authenticated user, never from the prompt.
Anything retrieved must already be something the user is allowed to read.
</details>

### 8. Where should PII be removed, and why there?

<details><summary>Answer</summary>

Before chunking and embedding. Once text is in an index, caches, logs and prompts, removal means
finding every copy. Use typed placeholders, test for false positives, and record which sources held
personal data so deletion requests (GDPR) can be honoured.
</details>

### 9. Duplicates in the knowledge base: why care?

<details><summary>Answer</summary>

They fill the top-k with the same text, crowding out the chunk that answers the question, and they
create conflicts when one copy is updated and the other is not. Remove exact duplicates with content
hashes and detect near duplicates with shingles and Jaccard (MinHash + LSH at scale).
</details>

### 10. The model answers confidently but wrongly. Where do you look?

<details><summary>Answer</summary>

First retrieval: was the right chunk retrieved at all (check recall for that question)? Then context
assembly: was it cut by the token budget, or drowned by weak matches below a sensible score threshold?
Then the prompt: does it instruct the model to answer only from sources and to say when it does not
know? Finally, validate citations so unsupported answers are flagged.
</details>
