# Database Architecture

The Helix Engineering Platform uses ClickHouse for high-volume analytical workloads and Redis for low-latency ephemeral data.

## ClickHouse

ClickHouse stores security and operational audit events that need to be queried across large time ranges.

The `audit_logs` dataset contains fields such as:

- event timestamp
- application identifier
- user identifier
- source IP address
- event type
- authentication result
- request ID

ClickHouse is used for analytical queries such as authentication trends, failed-login analysis, and security investigations.

Queries should filter on highly selective fields such as application ID and time range whenever possible.

## Redis

Redis is used for short-lived and low-latency application data.

Typical Redis use cases include:

- session-related data
- temporary rate-limit counters
- frequently accessed configuration
- short-lived coordination state

Redis data should not be treated as the permanent source of truth.

## Data Retention

Operational and security events have different retention requirements.

High-volume events are retained according to the platform's configured retention policy. Security-sensitive audit records are retained for longer periods when required for investigation and compliance.

## Query Performance

Analytical queries should avoid scanning unnecessary historical data.

For ClickHouse queries, filtering by timestamp and application identifier significantly reduces the amount of data that must be processed.

Services should also avoid requesting columns that are not required by the operation.

## Data Access

Database credentials and connection information are provided through environment-based configuration.

Credentials are never stored directly in source code or included in application logs.
