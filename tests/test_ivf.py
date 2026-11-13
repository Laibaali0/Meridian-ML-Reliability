import numpy as np
import pytest
from meridian.retrieval.ivf import IVFIndex


def test_full_probe_recovers_exact_neighbor():
    vectors = np.array([[0., 0.], [2., 2.], [5., 5.], [9., 9.]])
    index = IVFIndex(vectors, ["a", "b", "c", "d"], lists=2, seed=3)
    result = index.search(np.array([2., 2.]), k=2, probes=2)
    assert result[0] == ("b", 0.0)


def test_invalid_index_inputs_rejected():
    with pytest.raises(ValueError):
        IVFIndex(np.array([[1., 2.]]), ["x"], lists=2)
    with pytest.raises(ValueError):
        IVFIndex(np.array([[1., 2.], [2., 3.]]), ["x", "x"])


def test_empty_or_invalid_query_rejected():
    index = IVFIndex(np.eye(3), ["a", "b", "c"], lists=2)
    with pytest.raises(ValueError):
        index.search(np.array([1., 2.]))
