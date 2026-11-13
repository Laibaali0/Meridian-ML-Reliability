"""A seeded toy binary classification reliability report."""
import numpy as np
from .report import summarize_binary


def run(seed=42, n=400):
    if n < 2:
        raise ValueError("At least two samples required")
    rng = np.random.default_rng(seed)
    logits = rng.normal(size=n)
    probability = 1/(1+np.exp(-logits))
    labels = rng.binomial(1, probability)
    return {"synthetic_data": True, "seed": seed,
            "report": summarize_binary(labels, probability, seed=seed)}
