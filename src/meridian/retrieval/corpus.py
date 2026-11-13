"""Immutable document records with stable identifiers."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    doc_id: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


def check_corpus(documents):
    docs = list(documents)
    if not docs or any(not doc.doc_id for doc in docs):
        raise ValueError("Corpus needs documents with non-empty IDs")
    if len(set(doc.doc_id for doc in docs)) != len(docs):
        raise ValueError("Document IDs must be unique")
    return docs
