"""Append-only local JSONL experiment log; intentionally not concurrent-safe."""
import json
from pathlib import Path
from datetime import datetime, timezone
from .manifest import manifest


class Tracker:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, name, config, seed, metrics):
        if not metrics or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in metrics.values()):
            raise ValueError("Metrics must be nonempty numeric mapping")
        row = {**manifest(name, config, seed), "metrics": metrics,
               "recorded_utc": datetime.now(timezone.utc).isoformat()}
        with self.path.open("a", encoding="utf8") as stream:
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False)+"\n")
        return row

    def records(self):
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text().splitlines() if line.strip()]
