"""Structured metadata filters applied after ranking candidate IDs."""


def filter_documents(ranked_ids, documents, required=None, excluded=None):
    required = required or {}
    excluded = excluded or {}
    metadata = {doc.doc_id: doc.metadata for doc in documents}
    filtered = []
    for identifier in ranked_ids:
        if identifier not in metadata:
            continue
        meta = metadata[identifier]
        if any(meta.get(key) != value for key, value in required.items()):
            continue
        if any(meta.get(key) == value for key, value in excluded.items()):
            continue
        filtered.append(identifier)
    return filtered
