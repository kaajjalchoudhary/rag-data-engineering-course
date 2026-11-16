# 03 · Chunking

**Exercise:** [`exercises/m03_chunking.py`](../exercises/m03_chunking.py)

An embedding represents a whole chunk as one vector. Too large and the meaning blurs; too small and a
chunk loses the context needed to answer anything.

## Fixed-size windows

```python
fixed_size_chunks(text, size=500, overlap=50)
```

Simple and predictable. The overlap stops a fact that straddles a boundary from being lost entirely,
but windows still cut words and sentences in half.

## Structure-aware chunking

Pack whole **paragraphs** up to a size limit; only when a paragraph is too long, fall back to
**sentences**. Each chunk is then a coherent piece of text that reads well when cited.

| Approach | Pros | Cons |
|---|---|---|
| Fixed size + overlap | predictable size, trivial | cuts sentences, duplicates text |
| Paragraph / sentence packing | coherent, citeable | variable size |
| Heading-based sections | follows the author's structure | very uneven sizes |
| Semantic (embedding breakpoints) | splits on topic changes | slower, harder to test |

## Choosing a size

Start around 200 to 500 tokens, then **measure** with a golden question set (module 09). Prefix each
chunk with its document title when you embed it: "Warranty: The warranty does not cover water damage"
retrieves far better than the bare sentence.

## Stable chunk ids

Use ids like `warranty#0`, `warranty#1`. Stable ids are what let module 07 update one chunk instead of
re-embedding a whole document.
