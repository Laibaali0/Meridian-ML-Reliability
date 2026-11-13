"""Run read-only scripted tool evaluations; no LLM is called."""
from .cases import CASES
from .replay import replay
from .simulator import runtime
from .metrics import summary


def run():
    reports = [replay(case, runtime()) for case in CASES]
    return {"metrics": summary(reports), "reports": reports,
            "warning": "Deterministic replay; these outcomes are not agent model success rates"}
