"""Seeded bootstrap intervals for independent samples or matched pairs."""
import numpy as np


def mean_interval(values, repeats=1000, confidence=.95, seed=42):
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or not len(arr) or not np.isfinite(arr).all():
        raise ValueError("Expected finite non-empty scalar vector")
    if repeats < 2 or not 0 < confidence < 1:
        raise ValueError("Invalid bootstrap settings")
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, len(arr), size=(repeats, len(arr)))
    sampled = arr[draws].mean(axis=1)
    bounds = np.quantile(sampled, [(1-confidence)/2, 1-(1-confidence)/2])
    return {"mean": float(arr.mean()), "ci": [float(v) for v in bounds], "seed": seed}


def paired_difference(left, right, **kwargs):
    left, right = np.asarray(left, dtype=float), np.asarray(right, dtype=float)
    if left.shape != right.shape:
        raise ValueError("Paired metrics must have identical shapes")
    return mean_interval(left-right, **kwargs)
