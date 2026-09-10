from prometheus_client import Counter, Histogram

from app.core.metrics import (
    cache_hits_total,
    cache_misses_total,
    http_request_duration_seconds,
    http_requests_total,
    http_responses_total,
)


def test_http_requests_total_is_counter():
    assert isinstance(http_requests_total, Counter)


def test_http_responses_total_is_counter():
    assert isinstance(http_responses_total, Counter)


def test_http_request_duration_seconds_is_histogram():
    assert isinstance(http_request_duration_seconds, Histogram)


def test_cache_hits_metric_is_counter():
    assert isinstance(cache_hits_total, Counter)


def test_cache_misses_metric_is_counter():
    assert isinstance(cache_misses_total, Counter)
