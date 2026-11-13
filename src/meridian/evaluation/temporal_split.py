"""Chronological train/test split to avoid future-label leakage."""
from datetime import datetime


def chronological_split(timestamps, holdout_fraction=.2):
    times = list(timestamps)
    if len(times) < 2 or not 0 < holdout_fraction < 1:
        raise ValueError("Need >=2 timestamps and a holdout in (0,1)")
    if not all(isinstance(t, datetime) for t in times):
        raise ValueError("Times must be datetime objects")
    indexed = sorted(range(len(times)), key=lambda i: (times[i], i))
    test_size = max(1, min(len(times)-1, round(len(times)*holdout_fraction)))
    train, test = indexed[:-test_size], indexed[-test_size:]
    # Avoid splitting identical timestamps across train/test boundaries.
    boundary = times[test[0]]
    train = [i for i in indexed if times[i] < boundary]
    test = [i for i in indexed if times[i] >= boundary]
    if not train or not test:
        raise ValueError("Cannot create a leak-free split at this temporal boundary")
    return train, test
