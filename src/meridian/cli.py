"""Run independent experiments using deterministic synthetic fixtures."""
import argparse
import json
from pathlib import Path


def execute(command, seed=42):
    if command == "retrieval":
        from .retrieval.benchmark import benchmark
        return benchmark()
    if command == "serving":
        from .inference.benchmark import compare
        return compare(seed=seed)
    if command == "quantization":
        import numpy as np
        from .inference.quant_metrics import assess
        rng = np.random.default_rng(seed)
        weights = rng.normal(size=(128, 129)).astype(np.float32)
        data = rng.normal(size=(16, 129)).astype(np.float32)
        return {"seed": seed, "data": "synthetic weights and inputs", **assess(weights, data)}
    if command == "agents":
        from .agents.benchmark import run
        return run()
    if command == "temporal":
        from .temporal.benchmark import run
        return run()
    if command == "calibration":
        from .evaluation.benchmark import run
        return run(seed=seed)
    raise ValueError(f"Unknown experiment: {command}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=("retrieval", "serving", "quantization", "agents", "temporal", "calibration"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, help="Optional local output JSON")
    args = parser.parse_args(argv)
    result = {"experiment": args.experiment, "result": execute(args.experiment, args.seed)}
    content = json.dumps(result, indent=2, allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content + "\n")
    print(content)
    return result


if __name__ == "__main__":
    main()
