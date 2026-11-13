"""Tail-latency gaps across request priority groups."""
from collections import defaultdict
import numpy as np


def latency_by_priority(requests, completions):
    priorities = {request.id: request.priority for request in requests}
    groups = defaultdict(list)
    for row in completions:
        groups[priorities[row.request_id]].append(row.latency)
    return {str(priority): {"count": len(values), "p95_latency": float(np.quantile(values, .95))}
            for priority, values in sorted(groups.items())}
