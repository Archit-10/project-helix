# Application Caching

The Helix Engineering Platform uses an in-memory cache to reduce repeated computation for frequently requested data.

## Cache Strategy

The cache stores the results of expensive retrieval operations.

A cache entry is identified by a deterministic key derived from the request parameters.

For retrieval requests, the key includes the user query, requested result count, and applicable metadata filters.

Two requests with identical parameters therefore resolve to the same cache entry.

## Time-To-Live

Cached entries use a time-to-live (TTL) of five minutes.

After the TTL expires, the entry is treated as stale and the next request performs the underlying operation again.

The new result is then stored in the cache.

## Cache Invalidation

The retrieval cache is invalidated after successful knowledge-base indexing.

This prevents previously cached retrieval results from referencing stale search indexes.

Cache invalidation occurs only after indexing succeeds. If indexing fails, the existing cache remains unchanged.

## Cache Metrics

The platform records cache hits and misses using Prometheus metrics.

The primary metrics are:

- `cache_hits_total` — number of successful cache lookups.
- `cache_misses_total` — number of cache lookups that did not find a valid entry.

These metrics help operators understand cache effectiveness.

## Failure Behavior

The cache is an optimization and is not the source of truth for application data.

If the cache is unavailable or an entry is missing, the request continues by executing the underlying operation.

The application therefore remains functionally correct even when the cache provides no benefit.
