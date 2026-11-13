"""Memory-aware admission that refuses requests beyond capacity."""
from .kv_cache import KVCache


class AdmissionController:
    def __init__(self, cache: KVCache, max_inflight=16):
        if max_inflight < 1:
            raise ValueError("max_inflight must be positive")
        self.cache = cache
        self.max_inflight = max_inflight

    def admit(self, request):
        if request.id in self.cache.used:
            return False
        if len(self.cache.used) >= self.max_inflight:
            return False
        return self.cache.reserve(request.id, request.total_tokens)

    def complete(self, request_id):
        self.cache.release(request_id)
