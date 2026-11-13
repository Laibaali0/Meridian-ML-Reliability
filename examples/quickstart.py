"""Run all demo tracks and save compact JSON reports without a network call.

Usage from repository root (after editable install):
    python examples/quickstart.py
"""
from pathlib import Path
import json

from meridian.cli import execute


def main(output="outputs/overview.json"):
    experiments = ("retrieval", "serving", "quantization", "agents", "temporal", "calibration")
    results = {name: execute(name, seed=42) for name in experiments}
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(f"Saved {len(results)} experiment reports to {destination}")
    return results


if __name__ == "__main__":
    main()
