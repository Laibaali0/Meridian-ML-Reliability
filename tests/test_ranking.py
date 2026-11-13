import numpy as np
import pytest
from meridian.retrieval.metrics import recall_at_k, ndcg, reciprocal_rank
from meridian.retrieval.fusion import rrf, score_fusion
from meridian.retrieval.mmr import mmr
from meridian.retrieval.filters import filter_documents
from meridian.retrieval.corpus import Document


def test_known_ranking_metrics():
    truth = {"a": 3, "b": 1}
    assert recall_at_k(["z", "b"], truth, 2) == .5
    assert reciprocal_rank(["z", "b"], truth) == .5
    assert ndcg(["a", "b"], truth, 2) == pytest.approx(1)


def test_rank_fusion_is_repeatable():
    assert rrf([["a", "b"], ["b", "a"]]) == ["a", "b"]
    assert score_fusion([{"a": 0, "b": 1}, {"a": 1, "b": 0}]) == ["a", "b"]


def test_diversity_reranking_retains_unique_ids():
    ids = mmr([1, 0], np.array([[1, 0], [.99, .01], [0, 1.]]), ["a", "b", "c"], k=3)
    assert set(ids) == {"a", "b", "c"}


def test_metadata_filters_do_not_resurrect_missing_docs():
    docs = [Document("a", "text", {"version": "v1"}), Document("b", "text", {"version": "v2"})]
    assert filter_documents(["b", "a", "missing"], docs, required={"version": "v2"}) == ["b"]
