"""Tick-based continuous batching simulator with an explicit KV cache budget."""
from collections import deque
from dataclasses import dataclass

from .admission import AdmissionController
from .kv_cache import KVCache
from .policies import sort_queue


@dataclass
class Completion:
    request_id: str
    arrival: int
    started: int
    first_token: int
    finished: int
    output_tokens: int

    @property
    def latency(self):
        return self.finished - self.arrival

    @property
    def time_to_first_token(self):
        return self.first_token - self.arrival


class ContinuousBatchScheduler:
    """One decoder step per active sequence/tick; prefill is a fixed one-tick step.

    A sequence reserves its maximum projected KV memory on admission. This is a
    simplified discrete-event model; it does not implement an attention kernel.
    """
    def __init__(self, cache_blocks=256, block_tokens=16, max_inflight=8, policy="fifo"):
        self.controller = AdmissionController(KVCache(cache_blocks, block_tokens), max_inflight)
        self.policy = policy

    def run(self, requests, max_ticks=100000):
        requests = list(requests)
        if len({request.id for request in requests}) != len(requests):
            raise ValueError("Request IDs must be unique")
        for request in requests:
            if self.controller.cache.required(request.total_tokens) > self.controller.cache.capacity:
                raise ValueError(f"Request {request.id} cannot fit into KV cache")
        waiting = deque(sort_queue(requests, "fifo"))
        queued = []
        active = {}
        done = []
        clock = 0
        while waiting or queued or active:
            if clock >= max_ticks:
                raise TimeoutError("Simulation exceeded tick budget")
            while waiting and waiting[0].arrival <= clock:
                queued.append(waiting.popleft())
            queued = sort_queue(queued, self.policy)
            remaining = []
            for request in queued:
                if self.controller.admit(request):
                    active[request.id] = {"request": request, "started": clock, "emitted": 0}
                else:
                    remaining.append(request)
            queued = remaining
            for request_id, state in list(active.items()):
                state["emitted"] += 1
                if state["emitted"] >= state["request"].output_tokens:
                    request = state["request"]
                    done.append(Completion(request_id, request.arrival, state["started"],
                                           state["started"] + 1, clock + 1,
                                           request.output_tokens))
                    self.controller.complete(request_id)
                    del active[request_id]
            clock += 1
        return sorted(done, key=lambda row: row.request_id)
