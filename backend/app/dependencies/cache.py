from functools import lru_cache

from app.core.cache import Cache
from app.core.cache_memory import InMemoryCache


@lru_cache
def get_cache() -> Cache:
    return InMemoryCache()
