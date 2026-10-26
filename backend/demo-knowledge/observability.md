# Observability

The Helix Engineering Platform uses structured logs, metrics, and distributed tracing to monitor system health and investigate production issues.

## Structured Logging

Services generate structured JSON logs rather than unstructured text.

Each request log should include:

- request ID
- service name
- route or operation
- timestamp
- response status
- latency
- authenticated user identifier when available

Sensitive information such as passwords, access tokens, authorization headers, and database credentials must never be written to logs.

The request ID is propagated between services so that related log entries can be correlated during an investigation.

## Metrics

Services expose application and infrastructure metrics for monitoring.

Important application metrics include:

- request count
- request latency
- HTTP error count
- authentication failures
- authorization failures
- rate-limit events
- cache hits and misses
- Kafka consumer lag

Metrics are aggregated by service and operation where appropriate.

## Distributed Tracing

Distributed traces connect a request across multiple services.

A trace contains spans representing individual operations such as API gateway processing, authentication, authorization, retrieval, and downstream service calls.

Trace identifiers are propagated between services so that a slow or failed request can be followed across the system.

## API Gateway Monitoring

The API gateway records request latency, response status, route, and request ID.

A sudden increase in `401` responses may indicate authentication failures, while an increase in `403` responses may indicate authorization problems.

A large number of `429` responses indicates that clients are exceeding configured rate limits.

## Kafka Monitoring

Kafka consumers expose consumer-lag metrics.

Increasing consumer lag indicates that a consumer group is processing events slower than producers are publishing them.

For security events, sustained consumer lag can delay downstream risk analysis and security monitoring.

## Cache Monitoring

The platform records cache hits and misses using Prometheus metrics.

A declining cache-hit ratio may indicate that request patterns have changed, cache entries are expiring too quickly, or cache keys are not being reused effectively.

## Incident Investigation

Engineers typically investigate incidents by correlating metrics, traces, and structured logs.

A request ID can be used to locate the corresponding gateway and downstream service logs.

For security incidents, engineers can correlate authentication failures with Kafka security events and the corresponding audit records.

## Alerting

Alerts are configured for conditions that require operator attention.

Examples include:

- elevated HTTP error rates
- high request latency
- sustained Kafka consumer lag
- unusual authentication failure rates
- abnormal cache behavior

Alerts should identify the affected service and provide enough context for engineers to begin investigation quickly.
