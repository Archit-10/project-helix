from time import monotonic
from typing import Any

from app.core.cache import Cache
from app.core.metrics import cache_hits_total, cache_misses_total


class InMemoryCache(Cache):
    """In-memory cache implementation with TTL support."""

    def __init__(self) -> None:
        self._cache: dict[str, tuple[Any, float | None]] = {}

    def get(self, key: str) -> Any | None:
        """Returns a cached value if it exists and has not expired."""

        entry = self._cache.get(key)

        if entry is None:
            return None

        value, expires_at = entry

        if expires_at is not None and monotonic() >= expires_at:
            del self._cache[key]
            cache_misses_total.labels(cache="in_memory").inc()
            return None

        cache_hits_total.labels(cache="in_memory").inc()
        return value

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int | None = None,
    ) -> None:
        """Stores a value with an optional TTL."""

        expires_at = None

        if ttl_seconds is not None:
            expires_at = monotonic() + ttl_seconds

        self._cache[key] = (value, expires_at)

    def delete(self, key: str) -> None:
        """Deletes a cached value if it exists."""

        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clears all cached values."""

        self._cache.clear()
