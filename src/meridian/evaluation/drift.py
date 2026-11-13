"""Population stability index for numeric feature distribution shift."""
import numpy as np


def population_stability_index(reference, current, bins=10, epsilon=1e-6):
    reference, current = np.asarray(reference, dtype=float), np.asarray(current, dtype=float)
    if not len(reference) or not len(current) or bins < 2:
        raise ValueError("Need non-empty populations and at least two bins")
    if not np.isfinite(reference).all() or not np.isfinite(current).all():
        raise ValueError("Populations must be finite")
    edges = np.unique(np.quantile(reference, np.linspace(0, 1, bins+1)))
    if len(edges) < 2:
        return 0.0 if np.all(current == reference[0]) else float("inf")
    edges[0], edges[-1] = -np.inf, np.inf
    base, _ = np.histogram(reference, edges)
    recent, _ = np.histogram(current, edges)
    p = np.maximum(base/base.sum(), epsilon)
    q = np.maximum(recent/recent.sum(), epsilon)
    return float(np.sum((q-p)*np.log(q/p)))
