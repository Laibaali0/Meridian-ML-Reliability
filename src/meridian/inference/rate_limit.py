"""Discrete-time token bucket for admission and backpressure experiments."""


class TokenBucket:
    def __init__(self, capacity, refill_per_tick):
        if capacity <= 0 or refill_per_tick < 0:
            raise ValueError("Invalid capacity or refill rate")
        self.capacity = capacity
        self.refill = refill_per_tick
        self.tokens = float(capacity)
        self.tick = 0

    def allow(self, now, cost=1):
        if now < self.tick or cost <= 0:
            raise ValueError("Time cannot run backwards; cost must be positive")
        self.tokens = min(self.capacity, self.tokens + (now - self.tick) * self.refill)
        self.tick = now
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True
