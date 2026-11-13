"""Quantization comparisons that report memory and numerical error only."""
import numpy as np
from .quantize import pack, unpack


def assess(weights, inputs, group=32):
    w = np.asarray(weights, dtype=np.float32)
    x = np.asarray(inputs, dtype=np.float32)
    if x.ndim != 2 or x.shape[1] != w.shape[1]:
        raise ValueError("Input and weight dimensions differ")
    quantized = pack(w, group=group)
    restored = unpack(quantized)
    original_output = x @ w.T
    restored_output = x @ restored.T
    return {
        "fp32_bytes": int(w.nbytes),
        "int4_storage_bytes": quantized.bytes,
        "compression_ratio": float(w.nbytes / quantized.bytes),
        "mean_absolute_weight_error": float(abs(w - restored).mean()),
        "relative_output_l2_error": float(np.linalg.norm(original_output - restored_output) / max(np.linalg.norm(original_output), 1e-12)),
    }
