"""Block-granular KV cache reservation and release accounting."""
from math import ceil


class KVCache:
    def __init__(self, blocks, block_tokens=16):
        if blocks < 1 or block_tokens < 1:
            raise ValueError("Cache size and block size must be positive")
        self.capacity = blocks
        self.block_tokens = block_tokens
        self.used = {}

    @property
    def available(self):
        return self.capacity - sum(self.used.values())

    def required(self, tokens):
        if tokens < 1:
            raise ValueError("Tokens must be positive")
        return ceil(tokens / self.block_tokens)

    def reserve(self, request_id, tokens):
        blocks = self.required(tokens)
        old = self.used.get(request_id, 0)
        if blocks - old > self.available:
            return False
        self.used[request_id] = blocks
        return True

    def release(self, request_id):
        return self.used.pop(request_id, 0)
