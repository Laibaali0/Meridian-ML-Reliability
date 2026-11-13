"""Summary statistics for request latency and time-to-first-token."""
import numpy as np


def summarize(completions):
    data = list(completions)
    if not data:
        return {"requests": 0, "mean_latency": 0, "p95_latency": 0, "p95_ttft": 0}
    latencies = np.array([row.latency for row in data], dtype=float)
    ttft = np.array([row.time_to_first_token for row in data], dtype=float)
    return {
        "requests": len(data),
        "mean_latency": float(latencies.mean()),
        "p95_latency": float(np.quantile(latencies, .95)),
        "p95_ttft": float(np.quantile(ttft, .95)),
        "total_output_tokens": int(sum(row.output_tokens for row in data)),
    }
