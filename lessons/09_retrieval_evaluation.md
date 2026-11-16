# 09 · Evaluating retrieval

**Exercise:** [`exercises/m09_retrieval_evaluation.py`](../exercises/m09_retrieval_evaluation.py)

If retrieval misses the right chunk, no prompt engineering can save the answer. Measure retrieval on
its own, with a **golden set**: questions paired with the documents that answer them
(`data/golden_questions.json`).

## Metrics

| Metric | Question it answers |
|---|---|
| **recall@k** | Did the relevant documents appear in the top k? |
| **hit rate** | For what share of questions did *anything* relevant appear? |
| **MRR** (mean reciprocal rank) | How high did the first relevant result appear? 1 = always first |

Pick k to match what you actually send to the model. Recall@20 is irrelevant if the prompt only holds 4 chunks.

## Use it to decide

Change one thing at a time (chunk size, embedding model, hybrid on/off, re-ranker) and compare metrics
on the same golden set. Keep the evaluation in CI so a "harmless" change to cleaning cannot silently
drop recall.

## Building a golden set

Start with 30 to 50 real user questions from support tickets or search logs. Have a domain expert mark
the right source. Add every production failure as a new case: the golden set grows into a regression
suite.
