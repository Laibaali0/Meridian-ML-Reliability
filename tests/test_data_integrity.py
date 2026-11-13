from datetime import datetime, timezone, timedelta
import pytest
from meridian.evaluation.temporal_split import chronological_split
from meridian.evaluation.asof_join import point_in_time_join
from meridian.evaluation.manifest import fingerprint, manifest
from meridian.evaluation.checksums import sha256_file
from meridian.evaluation.tracker import Tracker
from meridian.evaluation.thresholds import check
from meridian.evaluation.slices import metrics_by_group


def test_temporal_holdout_excludes_same_timestamp_from_train():
    t = datetime(2025,1,1,tzinfo=timezone.utc)
    train, test = chronological_split([t, t+timedelta(days=1), t+timedelta(days=1), t+timedelta(days=2)], .5)
    assert train == [0]
    assert set(test) == {1,2,3}


def test_asof_feature_join_never_uses_future_values():
    assert point_in_time_join([("a", 4), ("a", 7), ("a", 1)],
                              [("a", 2, "past"), ("a", 6, "future")]) == ["past", "future", None]


def test_manifest_fingerprint_is_key_order_independent():
    assert fingerprint({"a":1,"b":2}) == fingerprint({"b":2,"a":1})
    assert manifest("test", {"a":1}, 4)["fingerprint"]


def test_tracker_round_trip_and_artifact_hash(tmp_path):
    path = tmp_path / "runs.jsonl"
    tracker = Tracker(path)
    tracker.record("example", {"seed":7}, 7, {"accuracy":.8})
    assert tracker.records()[0]["metrics"]["accuracy"] == .8
    assert len(sha256_file(path)) == 64


def test_gate_and_group_report():
    assert check({"accuracy":.7}, {"accuracy":(">=",.6)})["passed"]
    result = metrics_by_group([1,0,1,0], [1,0,0,1], ["A","A","B","B"])
    assert result["A"]["f1"] == 1
