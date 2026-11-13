"""Per-trace limits on tool calls and estimated resource usage."""


class Budget:
    def __init__(self, max_calls=8, max_units=100):
        if max_calls < 1 or max_units < 1:
            raise ValueError("Budget limits must be positive")
        self.max_calls, self.max_units = max_calls, max_units
        self.calls = 0
        self.units = 0

    def consume(self, units=1):
        if units < 0:
            raise ValueError("Consumed units cannot be negative")
        if self.calls + 1 > self.max_calls or self.units + units > self.max_units:
            return False
        self.calls += 1
        self.units += units
        return True
