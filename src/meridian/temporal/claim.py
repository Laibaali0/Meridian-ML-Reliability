"""Individual technical claims and explicit evidence links."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    claim_id: str
    api: str
    statement: str
    target_version: str
    target_date: str

    def __post_init__(self):
        if not self.claim_id or not self.api or not self.statement:
            raise ValueError("Claims need ID, API symbol and statement")


@dataclass(frozen=True)
class Evidence:
    claim_id: str
    source_id: str
    stance: str
    relevance: float

    def __post_init__(self):
        if self.stance not in ("supports", "refutes") or not 0 <= self.relevance <= 1:
            raise ValueError("Evidence stance or relevance is invalid")
