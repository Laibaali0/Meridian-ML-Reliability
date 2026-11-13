"""Canonicalize near-identical claim texts conservatively."""
import re
from collections import defaultdict


def normalize(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def group_claims(claims):
    grouped = defaultdict(list)
    for claim in claims:
        key = (claim.api, claim.target_version, normalize(claim.statement))
        grouped[key].append(claim.claim_id)
    return dict(grouped)
