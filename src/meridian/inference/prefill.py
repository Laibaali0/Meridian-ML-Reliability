"""Stylized prefill timing with per-token and fixed overhead costs."""
from math import ceil


def prefill_ticks(prompt_tokens, max_tokens_per_tick=256, setup_ticks=1):
    if prompt_tokens < 1 or max_tokens_per_tick < 1 or setup_ticks < 0:
        raise ValueError("Invalid prefill timing inputs")
    return ceil(prompt_tokens / max_tokens_per_tick) + setup_ticks


def batch_prefill_ticks(prompt_lengths, max_tokens_per_tick=256, setup_ticks=1):
    lengths = list(prompt_lengths)
    if not lengths:
        return 0
    if any(n <= 0 for n in lengths):
        raise ValueError("Prompt lengths must be positive")
    return prefill_ticks(sum(lengths), max_tokens_per_tick, setup_ticks)
