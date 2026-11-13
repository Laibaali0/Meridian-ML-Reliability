"""Evaluate traces by comparing observed outputs against expected fixtures."""
from .runtime import ToolFailure


def replay(trace, runtime):
    outcomes = []
    for step in trace.steps:
        try:
            value = runtime.call(step.tool, step.arguments)
            passed = not step.expected_error and value == step.expected
            outcomes.append({"tool": step.tool, "passed": bool(passed), "status": "ok"})
        except ToolFailure as exc:
            passed = bool(step.expected_error and str(exc) == step.expected_error)
            outcomes.append({"tool": step.tool, "passed": passed, "status": str(exc)})
    return {"trace": trace.name, "passed": all(row["passed"] for row in outcomes),
            "steps": outcomes, "audit": runtime.audit.counts()}
