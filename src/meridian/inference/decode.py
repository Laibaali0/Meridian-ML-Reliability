"""A deterministic decode progress counter, not an actual language model."""
from dataclasses import dataclass


@dataclass
class DecodeState:
    request_id: str
    target_tokens: int
    emitted: int = 0

    def step(self, tokens=1):
        if tokens < 0:
            raise ValueError("Cannot reverse decode progress")
        self.emitted = min(self.target_tokens, self.emitted + tokens)
        return self.complete

    @property
    def complete(self):
        return self.emitted >= self.target_tokens
