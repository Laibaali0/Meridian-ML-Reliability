import pytest
from meridian.inference.kv_cache import KVCache
from meridian.inference.admission import AdmissionController
from meridian.inference.request import Request
from meridian.inference.rate_limit import TokenBucket
from meridian.inference.memory import kv_cache_bytes, kv_cache_blocks
from meridian.inference.decode import DecodeState


def test_kv_cache_reservation_and_release():
    cache = KVCache(blocks=2, block_tokens=8)
    assert cache.reserve("a", 13)
    assert cache.available == 0
    assert not cache.reserve("b", 1)
    assert cache.release("a") == 2
    assert cache.available == 2


def test_admission_checks_concurrency():
    admission = AdmissionController(KVCache(50), max_inflight=1)
    assert admission.admit(Request("a", 0, 10, 2))
    assert not admission.admit(Request("b", 0, 10, 2))


def test_token_bucket_refills_without_time_reversal():
    limiter = TokenBucket(2, 1)
    assert limiter.allow(0) and limiter.allow(0)
    assert not limiter.allow(0)
    assert limiter.allow(1)
    with pytest.raises(ValueError):
        limiter.allow(0)


def test_memory_formula_and_decode_progress():
    assert kv_cache_bytes(2, 4, 8, 16) == 2 * 2 * 4 * 8 * 16 * 2
    assert kv_cache_blocks(17, 16) == 2
    decode = DecodeState("id", 3)
    assert not decode.step(2)
    assert decode.step(1)
