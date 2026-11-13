"""Per-row groupwise packed 4-bit weight quantization reference."""
from dataclasses import dataclass
from math import ceil
import numpy as np


@dataclass(frozen=True)
class Int4Weights:
    packed: np.ndarray
    scales: np.ndarray
    columns: int
    group: int

    @property
    def bytes(self):
        return int(self.packed.nbytes + self.scales.nbytes)


def pack(weights, group=32):
    arr = np.asarray(weights, dtype=np.float32)
    if arr.ndim != 2 or not arr.size or not np.isfinite(arr).all() or group < 1:
        raise ValueError("Expected finite non-empty matrix and positive group")
    rows, columns = arr.shape
    groups = ceil(columns / group)
    padded = np.pad(arr, ((0, 0), (0, groups * group - columns)))
    blocks = padded.reshape(rows, groups, group)
    scales = np.maximum(abs(blocks).max(axis=2) / 7, 1e-12).astype(np.float32)
    q = np.clip(np.rint(blocks / scales[:, :, None]), -7, 7).astype(np.int8).reshape(rows, -1)
    if q.shape[1] % 2:
        q = np.pad(q, ((0, 0), (0, 1)))
    bits = (q.astype(np.int16) + 8).astype(np.uint8)
    return Int4Weights(bits[:, ::2] | (bits[:, 1::2] << 4), scales, columns, group)


def unpack(model: Int4Weights):
    rows = len(model.packed)
    bits = np.empty((rows, model.packed.shape[1] * 2), dtype=np.float32)
    bits[:, ::2] = (model.packed & 15).astype(np.int16) - 8
    bits[:, 1::2] = ((model.packed >> 4) & 15).astype(np.int16) - 8
    groups = model.scales.shape[1]
    padded_columns = groups * model.group
    blocks = bits[:, :padded_columns].reshape(rows, groups, model.group)
    return (blocks * model.scales[:, :, None]).reshape(rows, padded_columns)[:, :model.columns]
