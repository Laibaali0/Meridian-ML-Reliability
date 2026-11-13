"""Ranking metrics for held-out query judgments."""
from math import log2


def recall_at_k(rank, relevant, k):
    if k < 1:
        raise ValueError("k must be positive")
    positives = {doc_id for doc_id, grade in relevant.items() if grade > 0}
    return len(set(rank[:k]) & positives) / len(positives) if positives else 0.0


def reciprocal_rank(rank, relevant):
    return next((1 / position for position, doc_id in enumerate(rank, 1) if relevant.get(doc_id, 0) > 0), 0.0)


def ndcg(rank, relevant, k=10):
    if k < 1 or any(grade < 0 for grade in relevant.values()):
        raise ValueError("k must be positive and grades nonnegative")
    def dcg(grades):
        return sum((2**grade - 1) / log2(i + 2) for i, grade in enumerate(grades))
    ideal = dcg(sorted(relevant.values(), reverse=True)[:k])
    observed = dcg([relevant.get(doc_id, 0) for doc_id in rank[:k]])
    return observed / ideal if ideal else 0.0
