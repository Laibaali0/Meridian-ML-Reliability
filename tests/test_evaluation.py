import numpy as np
import pytest
from meridian.evaluation.classification import binary_metrics
from meridian.evaluation.calibration import brier, ece
from meridian.evaluation.bootstrap import mean_interval, paired_difference
from meridian.evaluation.drift import population_stability_index
from meridian.evaluation.divergence import js_divergence
from meridian.evaluation.report import summarize_binary


def test_binary_confusion_metrics():
    result = binary_metrics([1,1,0,0], [1,0,1,0])
    assert result["tp"] == result["fp"] == result["fn"] == result["tn"] == 1
    assert result["f1"] == .5


def test_probabilities_are_calibrated_when_perfect():
    assert brier([0,1], [0,1]) == 0
    assert ece([0,1], [0,1]) == 0


def test_bootstrap_with_seed_is_repeatable():
    assert mean_interval([1,2,3], seed=3) == mean_interval([1,2,3], seed=3)
    diff = paired_difference([.9,.6], [.5,.4], seed=3)
    assert diff["mean"] == pytest.approx(.3)


def test_divergence_is_zero_for_same_distribution():
    assert js_divergence([1,2,3], [1,2,3]) == pytest.approx(0)


def test_population_stability_detects_shift():
    rng = np.random.default_rng(4)
    baseline = rng.normal(size=2000)
    assert population_stability_index(baseline, baseline) == pytest.approx(0)
    assert population_stability_index(baseline, baseline+2) > .5


def test_combined_calibration_report():
    report = summarize_binary([1, 0, 1, 0], [.8,.2,.7,.3], seed=3)
    assert report["n"] == 4
    assert 0 <= report["ece"] <= 1
