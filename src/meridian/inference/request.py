"""Immutable, validated request specifications for serving simulations."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    id: str
    arrival: int
    prompt_tokens: int
    output_tokens: int
    priority: int = 0

    def __post_init__(self):
        if not self.id or self.arrival < 0 or self.prompt_tokens < 1 or self.output_tokens < 1:
            raise ValueError("Request requires ID, nonnegative arrival and positive token counts")

    @property
    def total_tokens(self):
        return self.prompt_tokens + self.output_tokens
