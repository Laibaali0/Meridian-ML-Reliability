from meridian.temporal.benchmark import run
from meridian.temporal.dataset import example
from meridian.temporal.report import make_report
from meridian.temporal.citations import citations
from meridian.temporal.evidence import score_claim
from meridian.temporal.dedup import group_claims


def test_migration_report_has_support_and_refutation():
    result = run()
    assert result["claim_count"] == 2
    assert result["decisions"]["supported"] == 1
    assert result["decisions"]["refuted"] == 1


def test_citations_exclude_inapplicable_sources():
    sources, claims, links = example()
    result = score_claim(claims[1], sources, links)
    assert citations(result, "supports") == []
    assert len(citations(result, "refutes")) == 1


def test_claim_dedup_respects_api_and_version():
    sources, claims, links = example()
    assert len(group_claims(claims)) == 2
    assert make_report(sources, claims, links)["claim_count"] == 2
