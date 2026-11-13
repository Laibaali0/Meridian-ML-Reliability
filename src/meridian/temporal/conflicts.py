"""Identify competing support and refutation for review."""


def conflicts(scored_claims, threshold=.3):
    if threshold < 0:
        raise ValueError("threshold must be nonnegative")
    return [row["claim_id"] for row in scored_claims
            if row["support"] >= threshold and row["refute"] >= threshold]
