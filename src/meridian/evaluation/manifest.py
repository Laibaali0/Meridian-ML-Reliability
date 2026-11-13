"""Canonical fingerprints for reproducible experiment configurations."""
import hashlib
import json


def fingerprint(config):
    payload = json.dumps(config, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def manifest(name, config, seed, artifacts=None):
    if not name or not isinstance(seed, int):
        raise ValueError("Name and integer seed required")
    return {"name": name, "seed": seed, "config": config,
            "fingerprint": fingerprint({"config": config, "seed": seed}),
            "artifacts": artifacts or {}}
