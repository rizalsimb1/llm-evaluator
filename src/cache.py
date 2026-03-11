"""In-memory response cache with TTL support."""
import time
from typing import Any, Optional


class ResponseCache:
    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        self._store: dict = {}
        self.ttl = ttl_seconds
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, expires_at = self._store[key]
            if time.time() < expires_at:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: Any) -> None:
        if len(self._store) >= self.max_size:
            oldest = min(self._store, key=lambda k: self._store[k][1])
            del self._store[oldest]
        self._store[key] = (value, time.time() + self.ttl)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)
