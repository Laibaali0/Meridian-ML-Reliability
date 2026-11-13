"""Heuristic prompt-injection markers for untrusted tool output.

Heuristics are not a complete defense; data isolation and permissions remain
necessary even when these checks find no suspicious strings.
"""
import re

_MARKERS = [re.compile(pattern, re.I) for pattern in (
    r"ignore (all |your )?(previous|prior|system) instructions",
    r"reveal (your )?(system prompt|api key|secret)",
    r"disable (the )?(safety|security) checks",
)]


def suspicious_spans(text):
    return [match.group(0) for marker in _MARKERS for match in marker.finditer(str(text))]
