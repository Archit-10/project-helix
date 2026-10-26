# Helix Demo Knowledge Base

This directory contains the curated engineering knowledge base used by the public Helix demo.

The documents describe a fictional engineering platform and are intentionally designed to demonstrate retrieval, ranking, grounding, and citation behavior.

## Documents

- `authentication.md` — JWT authentication, token expiration, failed-login handling, and security events.
- `authorization.md` — RBAC, permissions, least privilege, and authorization failures.
- `api-gateway.md` — request flow, authentication, authorization, rate limiting, routing, and gateway observability.
- `kafka.md` — Kafka topics, consumer groups, offsets, reliability, and security-event processing.
- `caching.md` — retrieval caching, TTL, invalidation, and cache metrics.
- `database.md` — ClickHouse analytics, Redis usage, query performance, and data access.
- `observability.md` — structured logging, metrics, tracing, Kafka monitoring, and incident investigation.
- `retrieval.md` — BM25, vector search, hybrid retrieval, ranking, metadata filtering, and citations.
- `indexing.md` — ingestion, normalization, chunking, embeddings, vector indexes, and keyword indexes.
- `llm-generation.md` — grounded generation, retrieved context, citations, streaming, and failure handling.

## Purpose

The corpus is intentionally small enough to ship with the public demo while containing relationships across multiple engineering domains.

Example cross-document questions include:

- How does the API gateway authenticate and authorize requests?
- What happens after five failed login attempts?
- How are security events processed through Kafka?
- How does Helix combine keyword and vector retrieval?
- Why is the retrieval cache invalidated after indexing?
- How can an engineer investigate increasing Kafka consumer lag?
- How are generated answers connected to their supporting documents?
- What happens when the retrieved context is insufficient to answer a question?

## Demo Data

This corpus is reference data for the public demonstration environment. It should not be interpreted as documentation for a production Helix deployment.
