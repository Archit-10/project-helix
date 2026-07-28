# Architecture Decision Records (ADRs)

**ADR-001: Core tech-stack**

Date: 2026-07-28

Decision: Decided to standardize on the following:

1). **Web Framework:** FastAPI  
2). **Application Server:** Uvicorn  
3). **Configuration Management:** pydantic-settings  
4). **Testing Suite:** pytest + pytest-asyncio + httpx  
5). **Quality & Tooling:** ruff + pre-commit

**ADR-002: Package Manager Selection (uv)**

Date: 2026-07-28

Decision: Selected uv over pip/poetry.

Reason: uv provides faster package resolution, lockfile support, and clean environment isolation.
