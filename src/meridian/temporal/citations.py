"""Render citation references only for applicable, relevant source links."""


def citations(result, stance="supports"):
    if stance not in ("supports", "refutes"):
        raise ValueError("Invalid evidence stance")
    seen, links = set(), []
    for record in result["evidence"]:
        if record["applicable"] and record["stance"] == stance and record["source_id"] not in seen:
            seen.add(record["source_id"])
            links.append({"source_id": record["source_id"], "url": record["url"]})
    return links
