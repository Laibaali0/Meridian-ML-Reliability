import pytest
from meridian.inference.request import Request
from meridian.inference.scheduler import ContinuousBatchScheduler
from meridian.inference.latency import summarize
from meridian.inference.benchmark import compare
from meridian.inference.policies import sort_queue
from meridian.inference.sla import slo_report


def test_scheduler_finishes_requests_with_bounded_memory():
    jobs = [Request("a", 0, 16, 3), Request("b", 0, 32, 5), Request("c", 2, 16, 2)]
    result = ContinuousBatchScheduler(cache_blocks=8, block_tokens=16, max_inflight=2).run(jobs)
    assert {row.request_id for row in result} == {"a", "b", "c"}
    assert all(row.finished > row.started >= row.arrival for row in result)


def test_summary_and_slo_report():
    rows = ContinuousBatchScheduler().run([Request("a", 0, 4, 3)])
    report = summarize(rows)
    assert report["requests"] == 1
    assert slo_report(rows, max_ttft=1, max_latency=10)["pass_rate"] == 1


def test_priority_sorting():
    rows = [Request("a", 0, 4, 5, 0), Request("b", 0, 4, 2, 2)]
    assert sort_queue(rows, "priority")[0].id == "b"


def test_duplicate_request_ids_rejected():
    with pytest.raises(ValueError):
        ContinuousBatchScheduler().run([Request("a", 0, 4, 2), Request("a", 1, 4, 2)])


def test_policy_benchmark_uses_identical_workload():
    report = compare(seed=7, requests=12)
    assert report["requests"] == 12
    assert all(result["requests"] == 12 for result in report["policy_results"].values())


def test_oversized_request_fails_fast():
    with pytest.raises(ValueError, match="cannot fit"):
        ContinuousBatchScheduler(cache_blocks=1, block_tokens=4).run([Request("too-large", 0, 8, 8)])
