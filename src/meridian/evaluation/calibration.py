"""Brier score and expected calibration error for binary probabilities."""
import numpy as np


def _inputs(labels, probabilities):
    labels, p = np.asarray(labels, dtype=float), np.asarray(probabilities, dtype=float)
    if labels.shape != p.shape or labels.ndim != 1 or not len(labels):
        raise ValueError("Require aligned, non-empty vectors")
    if np.any((p < 0) | (p > 1)) or not np.isfinite(p).all() or not np.isin(labels, [0, 1]).all():
        raise ValueError("Expected 0/1 labels and probabilities in [0,1]")
    return labels, p


def brier(labels, probabilities):
    y, p = _inputs(labels, probabilities)
    return float(np.mean(np.square(y - p)))


def ece(labels, probabilities, bins=10):
    y, p = _inputs(labels, probabilities)
    if bins <= 0:
        raise ValueError("bins must be positive")
    edges = np.linspace(0, 1, bins+1)
    error = 0.0
    for i in range(bins):
        mask = (p >= edges[i]) & ((p < edges[i+1]) if i < bins-1 else (p <= edges[i+1]))
        if np.any(mask):
            error += mask.mean() * abs(y[mask].mean() - p[mask].mean())
    return float(error)
