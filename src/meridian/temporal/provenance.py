"""Trace each evidence decision to source title, date, and URL."""


def provenance_record(claim, source, evidence, applicable):
    if evidence.claim_id != claim.claim_id or evidence.source_id != source.source_id:
        raise ValueError("Evidence link refers to another claim or source")
    return {
        "claim_id": claim.claim_id,
        "source_id": source.source_id,
        "title": source.title,
        "url": source.url,
        "published": source.published.isoformat(),
        "stance": evidence.stance,
        "applicable": bool(applicable),
        "relevance": evidence.relevance,
    }
