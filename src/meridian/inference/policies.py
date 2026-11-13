"""Queue ordering rules for hypothetical inference workers."""


def sort_queue(requests, policy="fifo"):
    queue = list(requests)
    if policy == "fifo":
        return sorted(queue, key=lambda r: (r.arrival, r.id))
    if policy == "shortest":
        return sorted(queue, key=lambda r: (r.output_tokens, r.arrival, r.id))
    if policy == "priority":
        return sorted(queue, key=lambda r: (-r.priority, r.arrival, r.id))
    raise ValueError(f"Unknown scheduling policy: {policy}")
