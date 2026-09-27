from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests received.",
    ["method", "path"],
)

http_responses_total = Counter(
    "http_responses_total",
    "Total number of HTTP responses returned.",
    ["method", "path", "status_code"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)

cache_hits_total = Counter(
    "cache_hits_total",
    "Total number of cache hits.",
    ["cache"],
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total number of cache misses.",
    ["cache"],
)
