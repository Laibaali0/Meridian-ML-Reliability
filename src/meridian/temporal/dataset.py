"""Hand-authored miniature API migration timeline for tests and demos."""
from .claim import Claim, Evidence
from .intervals import parse_time, TimeWindow
from .source import Source


def example():
    sources = {
        "legacy": Source("legacy", "Legacy client API docs", parse_time("2024-01-01T00:00:00Z"),
                         TimeWindow(parse_time("2024-01-01T00:00:00Z"), parse_time("2025-01-01T00:00:00Z")),
                         ">=1.0,<2.0", "https://example.org/docs/v1"),
        "current": Source("current", "Current API migration guide", parse_time("2025-01-01T00:00:00Z"),
                          TimeWindow(parse_time("2025-01-01T00:00:00Z")), ">=2.0,<3.0",
                          "https://example.org/docs/v2"),
    }
    claims = [
        Claim("c1", "client.fetch", "Use fetch_v2 in the current release", "2.1", "2026-02-01T00:00:00Z"),
        Claim("c2", "client.fetch", "Use legacy_fetch in the current release", "2.1", "2026-02-01T00:00:00Z"),
    ]
    links = [
        Evidence("c1", "current", "supports", 1),
        Evidence("c2", "legacy", "supports", 1),
        Evidence("c2", "current", "refutes", 1),
    ]
    return sources, claims, links
