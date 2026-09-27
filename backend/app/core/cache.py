from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    """Abstract interface for application caching."""

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Returns the cached value for a key."""

    @abstractmethod
    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int | None = None,
    ) -> None:
        """Stores a value in the cache."""

    @abstractmethod
    def delete(self, key: str) -> None:
        """Deletes a cached value."""

    @abstractmethod
    def clear(self) -> None:
        """Clears all cached values."""
