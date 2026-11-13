"""Aggregate weighted evidence while excluding inapplicable sources."""
from .intervals import parse_time
from .provenance import provenance_record


def score_claim(claim, sources, evidence):
    date = parse_time(claim.target_date)
    records = []
    supported = refuted = 0.0
    for link in evidence:
        if link.claim_id != claim.claim_id:
            continue
        source = sources[link.source_id]
        applicable = source.applicable(date, claim.target_version)
        records.append(provenance_record(claim, source, link, applicable))
        if applicable:
            weight = source.reliability * link.relevance
            if link.stance == "supports":
                supported += weight
            else:
                refuted += weight
    return {"claim_id": claim.claim_id, "support": supported, "refute": refuted,
            "score": supported - refuted, "evidence": records}
