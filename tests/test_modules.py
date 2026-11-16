"""Checks each module. Run `pytest` for solutions, `COURSE_TARGET=exercises pytest -k m03` for yours."""

import pytest

from rag_course import load_documents, load_golden_questions

m = pytest.mark.module


# ---------- 01 cleaning ----------
@m("m01_cleaning")
def test_m01_normalize_text(mod):
    raw = "  Title\r\n\r\n\r\n\r\nLine with   spaces   \t\r\nnext\n\n\n"
    assert mod.normalize_text(raw) == "Title\n\nLine with spaces\nnext"


@m("m01_cleaning")
def test_m01_strip_markdown(mod):
    md = "# Returns FAQ\n**How long?** See [the policy](https://x.y/p) and *act fast*."
    assert mod.strip_markdown(md) == "Returns FAQ\nHow long? See the policy and act fast."


@m("m01_cleaning")
def test_m01_extract_title(mod):
    assert mod.extract_title(load_documents()["warranty"]) == "Warranty"
    assert mod.extract_title("no heading here") == ""


# ---------- 02 PII ----------
@m("m02_pii_redaction")
def test_m02_redact_pii(mod):
    text = "Mail jana.meyer@example-shop.com, call +49 30 1234567, pay to DE89 3704 0044 0532 0130 00."
    assert mod.redact_pii(text) == "Mail [EMAIL], call [PHONE], pay to [IBAN]."


@m("m02_pii_redaction")
def test_m02_keeps_ordinary_numbers(mod):
    text = "Refunds within 30 days, express before 14:00 costs 9.95 EUR."
    assert mod.redact_pii(text) == text


@m("m02_pii_redaction")
def test_m02_pii_report(mod):
    assert mod.pii_report(load_documents()["support_contacts"]) == {"email": 2, "iban": 0, "phone": 1}


# ---------- 03 chunking ----------
@m("m03_chunking")
def test_m03_fixed_size_chunks(mod):
    assert mod.fixed_size_chunks("abcdefghij", 4, 1) == ["abcd", "defg", "ghij"]
    assert mod.fixed_size_chunks("abcdefghij", 5, 0) == ["abcde", "fghij"]
    with pytest.raises(ValueError):
        mod.fixed_size_chunks("abc", 3, 3)


@m("m03_chunking")
def test_m03_structure_aware_chunks(mod):
    text = "Para one is short.\n\nPara two is short too.\n\nThird. It has two sentences."
    assert mod.structure_aware_chunks(text, 45) == [
        "Para one is short. Para two is short too.",
        "Third. It has two sentences.",
    ]
    long_paragraph = "First sentence here. Second sentence here. Third sentence here."
    assert mod.structure_aware_chunks(long_paragraph, 25) == [
        "First sentence here.", "Second sentence here.", "Third sentence here.",
    ]


@m("m03_chunking")
def test_m03_never_cuts_sentences(mod):
    for text in load_documents().values():
        for chunk in mod.structure_aware_chunks(text, 120):
            assert len(chunk) <= 120 or len(mod.split_sentences(chunk)) == 1


# ---------- 04 dedupe ----------
@m("m04_deduplication")
def test_m04_content_hash_ignores_formatting(mod):
    assert mod.content_hash("Refunds  within\n30 days") == mod.content_hash("refunds within 30 DAYS")
    assert mod.content_hash("a") != mod.content_hash("b")


@m("m04_deduplication")
def test_m04_dedupe_exact(mod):
    assert mod.dedupe_exact(["A b", "c", "a  B", "c", "d"]) == ["A b", "c", "d"]


@m("m04_deduplication")
def test_m04_jaccard_and_pairs(mod):
    assert mod.jaccard({1, 2, 3}, {2, 3, 4}) == 0.5
    assert mod.jaccard(set(), set()) == 0.0
    chunks = {
        "x": "customers can request a refund within 30 days of delivery",
        "y": "Customers can request a refund within 30 days of delivery!",
        "z": "express shipping costs 9.95 EUR",
    }
    assert mod.near_duplicate_pairs(chunks, 0.8) == [("x", "y", 1.0)]


# ---------- 05 embeddings ----------
@m("m05_embeddings")
def test_m05_tokenize(mod):
    assert mod.tokenize("How do I get my Refunds in 30 days?") == ["get", "refund", "30", "day"]


@m("m05_embeddings")
def test_m05_embed_properties(mod):
    v = mod.embed("refund within 30 days")
    assert len(v) == 256
    assert abs(sum(x * x for x in v) - 1.0) < 1e-9
    assert mod.embed("the and of") == [0.0] * 256
    assert mod.embed("Refunds") == mod.embed("refund")


@m("m05_embeddings")
def test_m05_cosine(mod):
    assert mod.cosine_similarity([1, 0], [1, 0]) == 1.0
    assert mod.cosine_similarity([1, 0], [0, 1]) == 0.0
    assert mod.cosine_similarity([0, 0], [1, 1]) == 0.0
    assert abs(mod.cosine_similarity([1, 1], [2, 2]) - 1.0) < 1e-9
    related = mod.cosine_similarity(mod.embed("refund policy days"), mod.embed("refund within 30 days"))
    unrelated = mod.cosine_similarity(mod.embed("refund policy days"), mod.embed("express shipping cost"))
    assert related > unrelated


# ---------- 06 vector index ----------
@m("m06_vector_index")
def test_m06_search_and_filter(mod):
    idx = mod.VectorIndex()
    idx.upsert("a", "Refunds are paid within 5 business days", {"lang": "en"})
    idx.upsert("b", "Express shipping costs 9.95 EUR", {"lang": "en"})
    idx.upsert("c", "Rückerstattung innerhalb von 5 Tagen refund", {"lang": "de"})
    assert len(idx) == 3
    assert [i for i, _ in idx.search("refund days", k=2)] == ["a", "c"]
    assert [i for i, _ in idx.search("refund days", k=2, where={"lang": "de"})] == ["c"]
    assert idx.search("warranty") == []
    idx.upsert("a", "Warranty covers defects")
    assert idx.search("warranty")[0][0] == "a"
    idx.delete("a")
    idx.delete("missing")
    assert len(idx) == 2


# ---------- 07 incremental ----------
@m("m07_incremental_indexing")
def test_m07_plan_sync(mod):
    from importlib import import_module
    h = import_module(mod.__name__.rsplit(".", 1)[0] + ".m04_deduplication").content_hash
    indexed = {"d#0": h("same"), "d#1": h("old text"), "d#2": h("gone")}
    current = {"d#0": "same", "d#1": "new text", "d#3": "brand new"}
    assert mod.plan_sync(current, indexed) == {
        "add": ["d#3"], "update": ["d#1"], "delete": ["d#2"], "unchanged": ["d#0"],
    }


@m("m07_incremental_indexing")
def test_m07_second_run_is_a_no_op(mod):
    from importlib import import_module
    VectorIndex = import_module(mod.__name__.rsplit(".", 1)[0] + ".m06_vector_index").VectorIndex
    docs = load_documents()
    current = {}
    for doc_id, text in docs.items():
        current.update(mod.chunk_document(doc_id, text))
    index, hashes = VectorIndex(), {}
    first = mod.apply_sync(index, current, hashes)
    assert first["add"] == len(current) and first["update"] == first["delete"] == 0
    assert mod.apply_sync(index, current, hashes) == {
        "add": 0, "update": 0, "delete": 0, "unchanged": len(current),
    }
    edited = dict(current)
    edited["shipping#0"] = edited["shipping#0"] + " Prices updated."
    del edited["warranty#0"]
    assert mod.apply_sync(index, edited, hashes) == {
        "add": 0, "update": 1, "delete": 1, "unchanged": len(current) - 2,
    }
    assert len(index) == len(current) - 1


# ---------- 08 hybrid ----------
@m("m08_hybrid_search")
def test_m08_bm25(mod):
    docs = {"a": "refund refund policy", "b": "shipping policy", "c": "warranty"}
    bm = mod.BM25(docs)
    hits = bm.search("refund policy")
    assert [d for d, _ in hits] == ["a", "b"]
    assert bm.idf("refund") > bm.idf("policy") > 0
    assert bm.search("unknown words") == []


@m("m08_hybrid_search")
def test_m08_rrf(mod):
    fused = mod.reciprocal_rank_fusion([["a", "b", "c"], ["b", "c", "d"]], k=60)
    assert [d for d, _ in fused] == ["b", "c", "a", "d"]
    assert fused[0][1] == round(1 / 62 + 1 / 61, 5)


# ---------- 09 evaluation ----------
@m("m09_retrieval_evaluation")
def test_m09_metrics(mod):
    assert mod.recall_at_k(["x", "a", "b"], {"a", "b"}, 2) == 0.5
    assert mod.recall_at_k(["x"], set(), 3) == 0.0
    assert mod.reciprocal_rank(["x", "y", "a"], {"a"}) == pytest.approx(1 / 3)
    assert mod.reciprocal_rank(["x"], {"a"}) == 0.0


@m("m09_retrieval_evaluation")
def test_m09_evaluate(mod):
    golden = [
        {"question": "q1", "relevant_doc": "a"},
        {"question": "q2", "relevant_doc": "b"},
        {"question": "q3", "relevant_doc": "c"},
        {"question": "q4", "relevant_doc": "d"},
    ]
    answers = {"q1": ["a", "x"], "q2": ["x", "b"], "q3": ["x", "y", "z", "c"], "q4": []}
    assert mod.evaluate(lambda q: answers[q], golden, k=3) == {
        "recall_at_k": 0.5, "mrr": 0.438, "hit_rate": 0.5,
    }


@m("m09_retrieval_evaluation")
def test_m09_golden_set_on_course_data(mod):
    """Whole pipeline: BM25 over the course documents finds the right document for every question."""
    from solutions.m08_hybrid_search import BM25
    bm = BM25(load_documents())
    result = mod.evaluate(lambda q: [d for d, _ in bm.search(q, k=5)], load_golden_questions(), k=3)
    assert result["recall_at_k"] == 1.0


# ---------- 10 grounded prompts ----------
@m("m10_grounded_prompts")
def test_m10_estimate_tokens(mod):
    assert mod.estimate_tokens("") == 0
    assert mod.estimate_tokens("abcd") == 1
    assert mod.estimate_tokens("abcde") == 2


@m("m10_grounded_prompts")
def test_m10_select_context(mod):
    chunks = {"a": "x" * 40, "b": "y" * 40, "c": "z" * 40, "d": "w" * 4}
    hits = [("a", 0.9), ("b", 0.8), ("d", 0.05), ("c", 0.7)]
    assert mod.select_context(hits, chunks, token_budget=20) == ["a", "b"]
    assert mod.select_context(hits, chunks, token_budget=100) == ["a", "b", "c"]
    assert mod.select_context([("d", 0.01)], chunks, token_budget=100) == []


@m("m10_grounded_prompts")
def test_m10_build_prompt_and_citations(mod):
    chunks = {"refund_policy#0": "Refunds within 30 days.", "shipping#0": "Express costs 9.95 EUR."}
    prompt = mod.build_prompt("How long?", ["refund_policy#0", "shipping#0"], chunks)
    assert "[1] (refund_policy#0) Refunds within 30 days." in prompt
    assert "[2] (shipping#0) Express costs 9.95 EUR." in prompt
    assert prompt.rstrip().endswith("Question: How long?\nAnswer:")
    assert mod.build_prompt("How long?", [], chunks) == ""
    assert mod.check_citations("30 days [1], see also [3] and [1].", 2) == {"valid": [1], "invalid": [3]}
