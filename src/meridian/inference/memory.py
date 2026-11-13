"""Estimate KV cache footprint from model dimensions and sequence length."""
from math import ceil


def kv_cache_bytes(layers, kv_heads, head_dim, tokens, bytes_per_element=2):
    if min(layers, kv_heads, head_dim, tokens, bytes_per_element) <= 0:
        raise ValueError("All KV dimensions must be positive")
    return 2 * layers * kv_heads * head_dim * tokens * bytes_per_element


def kv_cache_blocks(tokens, block_size=16):
    if tokens <= 0 or block_size <= 0:
        raise ValueError("Block sizes and tokens must be positive")
    return ceil(tokens / block_size)
