from unittest.mock import patch

from app.core.cache_memory import InMemoryCache
from app.core.metrics import cache_hits_total, cache_misses_total


def test_set_and_get():
    cache = InMemoryCache()

    cache.set("key", "value")

    assert cache.get("key") == "value"


def test_get_missing_key_returns_none():
    cache = InMemoryCache()

    assert cache.get("missing") is None


def test_delete_removes_value():
    cache = InMemoryCache()

    cache.set("key", "value")
    cache.delete("key")

    assert cache.get("key") is None


def test_clear_removes_all_values():
    cache = InMemoryCache()

    cache.set("key1", "value1")
    cache.set("key2", "value2")

    cache.clear()

    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_value_expires_after_ttl():
    cache = InMemoryCache()

    with patch(
        "app.core.cache_memory.monotonic",
        side_effect=[100.0, 100.5, 101.0],
    ):
        cache.set("key", "value", ttl_seconds=1)

        assert cache.get("key") == "value"
        assert cache.get("key") is None


def test_value_without_ttl_does_not_expire():
    cache = InMemoryCache()

    with patch(
        "app.core.cache_memory.monotonic",
        side_effect=[100.0, 200.0],
    ):
        cache.set("key", "value")
        assert cache.get("key") == "value"


def test_set_overwrites_existing_value():
    cache = InMemoryCache()

    cache.set("key", "value1")
    cache.set("key", "value2")

    assert cache.get("key") == "value2"


def test_delete_missing_key_is_safe():
    cache = InMemoryCache()

    cache.delete("missing")

    assert cache.get("missing") is None


def test_cache_hit_is_recorded():
    cache = InMemoryCache()

    cache.set("key", "value")
    cache.get("key")

    assert (
        cache_hits_total.labels(
            cache="in_memory",
        )._value.get()
        >= 1
    )


def test_cache_miss_is_recorded():
    cache = InMemoryCache()

    cache.get("missing")

    assert (
        cache_misses_total.labels(
            cache="in_memory",
        )._value.get()
        >= 1
    )
