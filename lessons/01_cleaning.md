# 01 · Loading and cleaning documents

**Exercise:** [`exercises/m01_cleaning.py`](../exercises/m01_cleaning.py)

Retrieval quality is decided before the first embedding is computed. Every invisible character,
duplicated header or broken line that enters the index becomes noise in every vector built from it.

## What to normalise

| Problem | Example | Fix |
|---|---|---|
| Unicode variants | non-breaking space ` `, full-width digits | `unicodedata.normalize("NFKC", text)` |
| Line endings | `\r\n` from Windows exports | convert to `\n` |
| Whitespace runs | `"Line   with \t spaces"` | collapse to one space |
| Empty-line blocks | 4 blank lines between sections | keep at most one blank line |
| Markup noise | `**bold**`, `# Heading`, `[text](url)` | keep the words, drop the syntax |

Keep **structure** you will use later: blank lines mark paragraph boundaries, which module 03 uses to
chunk on natural breaks. Normalise whitespace *inside* lines, not the line breaks themselves.

## Keep metadata, not just text

The title, source path, last-modified date and access level are metadata. Store them next to each
chunk: they power filters (module 06), citations (module 10) and incremental sync (module 07).

## In production

- PDFs and HTML need extraction first (pdfplumber / unstructured / trafilatura). Inspect the output:
  headers, footers and page numbers repeated on every page are a classic source of near-duplicates.
- Make cleaning a **pure function**: the same input always gives the same output. That is what makes
  content hashes, and therefore incremental re-indexing, reliable.
