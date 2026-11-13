"""Minimal Unicode-aware token normalization for retrieval fixtures."""
import re
import unicodedata


def tokens(text: str) -> list[str]:
    """Normalize case and combining characters before tokenization."""
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return re.findall(r"[^\W_]+", normalized, flags=re.UNICODE)


def term_counts(text: str) -> dict[str, int]:
    counts = {}
    for token in tokens(text):
        counts[token] = counts.get(token, 0) + 1
    return counts
