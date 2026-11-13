"""Summarize task completion, tool failures and expected denials."""


def summary(reports):
    rows = list(reports)
    if not rows:
        return {"total": 0, "pass_rate": 0.0, "step_pass_rate": 0.0}
    correct = sum(row["passed"] for row in rows)
    steps = [step for row in rows for step in row["steps"]]
    return {"total": len(rows), "passed": correct, "pass_rate": correct / len(rows),
            "total_steps": len(steps),
            "step_pass_rate": sum(step["passed"] for step in steps) / len(steps) if steps else 1.0,
            "blocked_steps": sum(step["status"] not in ("ok", "execution_failure") for step in steps)}
