"""Jensen-Shannon divergence between discrete probability distributions."""
import numpy as np


def js_divergence(p, q, epsilon=1e-12):
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    if p.shape != q.shape or p.ndim != 1 or not len(p):
        raise ValueError("Probability vectors must match")
    if (p < 0).any() or (q < 0).any() or p.sum() <= 0 or q.sum() <= 0:
        raise ValueError("Probability masses must be nonnegative and nonempty")
    p, q = p/p.sum(), q/q.sum()
    midpoint = (p+q)/2
    def kl(a, b):
        mask = a > 0
        return np.sum(a[mask]*np.log(a[mask]/np.maximum(b[mask], epsilon)))
    return float((kl(p, midpoint)+kl(q, midpoint))/2)
