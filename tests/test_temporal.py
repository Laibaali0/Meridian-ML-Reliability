import pytest
from meridian.temporal.version import Version
from meridian.temporal.constraints import VersionConstraint
from meridian.temporal.intervals import parse_time, TimeWindow
from meridian.temporal.dataset import example
from meridian.temporal.evidence import score_claim
from meridian.temporal.decision import classify


def test_version_ordering_and_constraints():
    assert Version.parse("v2.1") > Version.parse("1.9.9")
    assert VersionConstraint(">=2.0,<3.0").allows("2.5")
    assert not VersionConstraint(">=2.0,<3.0").allows("3.0")
    assert Version.parse("2.0.0-beta") < Version.parse("2.0.0")


def test_invalid_versions_rejected():
    with pytest.raises(ValueError):
        Version.parse("tomorrow")
    with pytest.raises(ValueError):
        VersionConstraint("^2.0")


def test_utc_validity_window_excludes_end():
    window = TimeWindow(parse_time("2025-01-01T00:00:00Z"), parse_time("2025-02-01T00:00:00Z"))
    assert window.contains(parse_time("2025-01-31T23:59:59Z"))
    assert not window.contains(parse_time("2025-02-01T00:00:00Z"))


def test_old_api_docs_not_used_for_current_target():
    sources, claims, evidence = example()
    legacy_claim = score_claim(claims[1], sources, evidence)
    assert classify(legacy_claim) == "refuted"
    assert legacy_claim["support"] == 0
    assert any(not row["applicable"] for row in legacy_claim["evidence"])
