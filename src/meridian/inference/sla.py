"""Service-level objective checks with explicit violation counts."""


def slo_report(completions, max_ttft, max_latency):
    if max_ttft <= 0 or max_latency <= 0:
        raise ValueError("Thresholds must be positive")
    rows = list(completions)
    if not rows:
        return {"total": 0, "ttft_violations": 0, "latency_violations": 0, "pass_rate": 1.0}
    ttft = sum(row.time_to_first_token > max_ttft for row in rows)
    late = sum(row.latency > max_latency for row in rows)
    passes = sum(row.time_to_first_token <= max_ttft and row.latency <= max_latency for row in rows)
    return {"total": len(rows), "ttft_violations": ttft,
            "latency_violations": late, "pass_rate": passes / len(rows)}
