"""Demonstrate version-aware evidence decisions on a fictional API timeline."""
from .dataset import example
from .report import make_report


def run():
    sources, claims, links = example()
    result = make_report(sources, claims, links)
    result["dataset"] = "Hand-authored fictional API migration"
    result["warning"] = "Not a validated model benchmark; relevance scores are provided, not inferred"
    return result
