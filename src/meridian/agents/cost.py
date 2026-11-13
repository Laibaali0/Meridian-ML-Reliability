"""Compute declared token/call budgets without billing claims."""


def estimated_cost(prompt_tokens, completion_tokens, input_price_per_million, output_price_per_million):
    args = (prompt_tokens, completion_tokens, input_price_per_million, output_price_per_million)
    if any(value < 0 for value in args):
        raise ValueError("Token counts and configured prices cannot be negative")
    return ((prompt_tokens * input_price_per_million + completion_tokens * output_price_per_million) / 1_000_000)
