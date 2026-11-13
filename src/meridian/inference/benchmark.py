"""Compare queue policies under the same synthetic token workload."""
from .scheduler import ContinuousBatchScheduler
from .workload import generate
from .latency import summarize


def compare(seed=42, requests=60):
    workload = generate(n=requests, seed=seed)
    reports = {}
    for policy in ("fifo", "priority", "shortest"):
        engine = ContinuousBatchScheduler(cache_blocks=160, max_inflight=6, policy=policy)
        reports[policy] = summarize(engine.run(workload))
    return {"seed": seed, "requests": len(workload), "policy_results": reports,
            "note": "Discrete-tick CPU simulation; not measured GPU serving performance"}
