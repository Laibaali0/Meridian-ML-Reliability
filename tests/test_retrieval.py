import pytest
from meridian.retrieval.corpus import Document
from meridian.retrieval.tokenize import tokens, term_counts
from meridian.retrieval.bm25 import BM25
from meridian.retrieval.hybrid import HybridSearch
from meridian.retrieval.benchmark import benchmark


def docs():
    return [Document("a", "GPU quantization improves memory use"),
            Document("b", "Shopping catalog ranking and search"),
            Document("c", "Evaluation of agent safety and tools")]


def test_tokenizer_handles_unicode_and_case():
    assert tokens("CAFÉ café") == ["café", "café"]
    assert term_counts("A A b") == {"a": 2, "b": 1}


def test_bm25_favors_matching_document():
    assert BM25(docs()).search("GPU memory")[0] == "a"


def test_invalid_bm25_and_corpus_rejected():
    with pytest.raises(ValueError):
        BM25([docs()[0], docs()[0]])
    with pytest.raises(ValueError):
        BM25(docs(), k1=-1)


def test_hybrid_methods_return_valid_documents():
    engine = HybridSearch(docs(), dimensions=2)
    for method in ("bm25", "latent", "hybrid"):
        result = engine.search("search ranking", method=method, k=2)
        assert len(result) == len(set(result)) == 2
        assert set(result).issubset({"a", "b", "c"})


def test_retrieval_benchmark_reports_all_baselines():
    report = benchmark()
    assert report["toy_queries"] == 3
    assert set(report["methods"]) == {"bm25", "latent", "hybrid"}
