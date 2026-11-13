import pytest
from meridian.agents.cases import CASES
from meridian.agents.simulator import runtime
from meridian.agents.replay import replay
from meridian.agents.benchmark import run
from meridian.agents.runtime import ToolFailure
from meridian.agents.metrics import summary


def test_all_reference_traces_pass():
    report = run()
    assert report["metrics"]["total"] == 4
    assert report["metrics"]["pass_rate"] == 1.0


def test_stale_or_unregistered_tool_is_denied():
    engine = runtime()
    with pytest.raises(ToolFailure, match="unregistered"):
        engine.call("invented_tool", {})
    assert engine.audit.counts()["blocked"] == 1


def test_delete_is_rejected_in_read_only_mode():
    engine = runtime()
    with pytest.raises(ToolFailure, match="writes_disabled"):
        engine.call("delete_product", {"sku": "ITEM-01"})


def test_trace_replay_is_deterministic():
    assert replay(CASES[0], runtime()) == replay(CASES[0], runtime())


def test_metrics_report_passes_and_denials_separately():
    reports = [replay(case, runtime()) for case in CASES]
    result = summary(reports)
    assert result["total_steps"] == 4
    assert result["blocked_steps"] == 2
