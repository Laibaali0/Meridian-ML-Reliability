"""Generate a compact model quality report with uncertainty intervals."""
from .classification import binary_metrics
from .calibration import brier, ece
from .bootstrap import mean_interval


def summarize_binary(labels, probabilities, threshold=.5, seed=42):
    if not 0 <= threshold <= 1:
        raise ValueError("Decision threshold must be within [0,1]")
    labels, probabilities = list(labels), list(probabilities)
    predicted = [int(value >= threshold) for value in probabilities]
    squared_errors = [(actual-prob)**2 for actual, prob in zip(labels, probabilities)]
    return {"threshold": threshold,
            "classification": binary_metrics(labels, predicted),
            "brier": brier(labels, probabilities),
            "ece": ece(labels, probabilities),
            "brier_bootstrap": mean_interval(squared_errors, seed=seed),
            "n": len(labels)}
