"""Compile a reproducible report over target-date technical claims."""
from .evidence import score_claim
from .decision import classify
from .risk import priority


def make_report(sources, claims, evidence):
    entries = []
    for claim in claims:
        scored = score_claim(claim, sources, evidence)
        entries.append({"claim_id": claim.claim_id,
                        "decision": classify(scored),
                        "priority": priority(scored),
                        "details": scored})
    entries.sort(key=lambda row: (-row["priority"], row["claim_id"]))
    return {"claims": entries, "claim_count": len(entries),
            "decisions": {label: sum(row["decision"] == label for row in entries)
                          for label in ("supported", "refuted", "conflicted", "insufficient_evidence")}}
