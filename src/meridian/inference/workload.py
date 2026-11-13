"""Seeded request traffic generators for repeatable load experiments."""
import numpy as np
from .request import Request


def generate(n=80, seed=42, burst=4):
    if n < 1 or burst < 1:
        raise ValueError("n and burst must be positive")
    rng = np.random.default_rng(seed)
    arrivals = np.cumsum(rng.poisson(1, size=n) // burst)
    return [Request(f"req-{i:04d}", int(arrivals[i]),
                    int(rng.integers(16, 129)), int(rng.integers(4, 33)),
                    int(rng.integers(0, 3))) for i in range(n)]
