import numpy as np
import pytest
from meridian.inference.quantize import pack, unpack
from meridian.inference.quant_metrics import assess
from meridian.inference.prefill import prefill_ticks, batch_prefill_ticks


@pytest.mark.parametrize("shape,group", [((3,5),4), ((1,1),1), ((20,32),16), ((7,67),32)])
def test_packed_int4_roundtrip_has_correct_shape(shape, group):
    weights = np.random.default_rng(42).normal(size=shape).astype("float32")
    assert unpack(pack(weights, group)).shape == shape


def test_zero_matrix_exact_reconstruction():
    weights = np.zeros((4, 29), dtype="float32")
    np.testing.assert_array_equal(unpack(pack(weights)), weights)


def test_groupwise_quantization_reduces_weight_storage():
    rng = np.random.default_rng(8)
    weights = rng.normal(size=(128,128)).astype("float32")
    report = assess(weights, rng.normal(size=(8,128)), group=16)
    assert report["compression_ratio"] > 1
    assert report["relative_output_l2_error"] < .25


def test_nonfinite_weights_fail_validation():
    with pytest.raises(ValueError):
        pack([[float("nan"), 1]])


def test_prefill_cost_grows_with_prompt_volume():
    assert prefill_ticks(512) > prefill_ticks(128)
    assert batch_prefill_ticks([128,128]) >= prefill_ticks(128)
