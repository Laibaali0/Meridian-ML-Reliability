"""Risk-based prioritization of stale or unsupported claims."""


def priority(result, impact=1.0):
    if impact < 0:
        raise ValueError("impact must be nonnegative")
    active = [record for record in result["evidence"] if record["applicable"]]
    obsolete = [record for record in result["evidence"] if not record["applicable"]]
    uncertainty = 1 / (1 + abs(result["support"] - result["refute"]))
    return impact * (uncertainty + len(obsolete) / (1 + len(active)))
