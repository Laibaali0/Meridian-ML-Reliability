"""Conservative three-way classification of technical claims."""


def classify(result, margin=.25, min_evidence=.5):
    if margin < 0 or min_evidence < 0:
        raise ValueError("Margins must be nonnegative")
    support, refute = result["support"], result["refute"]
    if max(support, refute) < min_evidence:
        return "insufficient_evidence"
    if support - refute >= margin:
        return "supported"
    if refute - support >= margin:
        return "refuted"
    return "conflicted"
