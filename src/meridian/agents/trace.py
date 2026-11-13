"""Validated tool trace objects independent of any language-model provider."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TraceStep:
    tool: str
    arguments: dict
    expected: object = None
    expected_error: str = ""


@dataclass(frozen=True)
class Trace:
    name: str
    steps: tuple[TraceStep, ...]


def load_cases(records):
    cases = []
    for record in records:
        if not record.get("name") or not isinstance(record.get("steps"), list):
            raise ValueError("Trace requires a name and ordered steps")
        steps = []
        for step in record["steps"]:
            if "tool" not in step or "arguments" not in step:
                raise ValueError("Trace step requires tool and arguments")
            steps.append(TraceStep(step["tool"], step["arguments"],
                                   step.get("expected"), step.get("expected_error", "")))
        cases.append(Trace(record["name"], tuple(steps)))
    return cases
