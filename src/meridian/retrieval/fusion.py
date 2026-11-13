"""Reciprocal rank fusion and normalized weighted score fusion."""


def rrf(rankings, offset=60):
    if offset < 0:
        raise ValueError("offset must be nonnegative")
    combined = {}
    for ranking in rankings:
        if len(ranking) != len(set(ranking)):
            raise ValueError("Ranking has duplicate IDs")
        for rank, identifier in enumerate(ranking, 1):
            combined[identifier] = combined.get(identifier, 0) + 1 / (offset + rank)
    return sorted(combined, key=lambda key: (-combined[key], key))


def score_fusion(score_maps, weights=None):
    if not score_maps:
        raise ValueError("At least one score source required")
    weights = [1.0] * len(score_maps) if weights is None else list(weights)
    if len(weights) != len(score_maps) or any(w < 0 for w in weights):
        raise ValueError("Weights must be nonnegative and align with sources")
    combined = {}
    for score_map, weight in zip(score_maps, weights):
        if not score_map:
            continue
        values = list(score_map.values())
        low, high = min(values), max(values)
        for doc_id, score in score_map.items():
            normalized = (score - low) / (high - low) if high > low else 0
            combined[doc_id] = combined.get(doc_id, 0) + weight * normalized
    return sorted(combined, key=lambda key: (-combined[key], key))
