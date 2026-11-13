"""Maximal marginal relevance reranking with a diversity penalty."""
import numpy as np


def mmr(query_vector, candidate_vectors, identifiers, k=5, relevance_weight=.7):
    query = np.asarray(query_vector, dtype=float)
    vectors = np.asarray(candidate_vectors, dtype=float)
    if vectors.ndim != 2 or vectors.shape[0] != len(identifiers) or len(set(identifiers)) != len(identifiers):
        raise ValueError("Candidate vectors and IDs must align and be unique")
    if vectors.shape[1] != len(query) or not 0 <= relevance_weight <= 1 or k < 1:
        raise ValueError("Invalid vectors, k, or relevance weight")
    normalized = vectors / np.maximum(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-12)
    normalized_query = query / max(np.linalg.norm(query), 1e-12)
    relevance = normalized @ normalized_query
    similarities = normalized @ normalized.T
    chosen = []
    remaining = set(range(len(identifiers)))
    while remaining and len(chosen) < k:
        def score(i):
            redundancy = max((similarities[i, j] for j in chosen), default=0.0)
            return relevance_weight * relevance[i] - (1 - relevance_weight) * redundancy
        best = min(remaining, key=lambda i: (-score(i), identifiers[i]))
        chosen.append(best)
        remaining.remove(best)
    return [identifiers[i] for i in chosen]
