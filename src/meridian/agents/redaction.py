"""Conservative redaction for diagnostic traces and reports."""
import re

_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*([A-Za-z0-9_-]{8,})"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
]


def redact(text):
    value = str(text)
    value = _PATTERNS[0].sub(lambda match: f"{match[1]}=[REDACTED]", value)
    return _PATTERNS[1].sub("[EMAIL]", value)
