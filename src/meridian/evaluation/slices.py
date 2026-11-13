"""Report metrics for predeclared groups instead of hiding average failures."""
from collections import defaultdict
from .classification import binary_metrics


def metrics_by_group(labels, predictions, group_labels, min_count=1):
    labels, predictions, group_labels = list(labels), list(predictions), list(group_labels)
    if len(labels) != len(predictions) or len(labels) != len(group_labels):
        raise ValueError("Vectors must align")
    if min_count < 1:
        raise ValueError("min_count must be positive")
    groups = defaultdict(list)
    for i, name in enumerate(group_labels):
        groups[str(name)].append(i)
    return {name: {"samples": len(indices), **binary_metrics([labels[i] for i in indices], [predictions[i] for i in indices])}
            for name, indices in sorted(groups.items()) if len(indices) >= min_count}
