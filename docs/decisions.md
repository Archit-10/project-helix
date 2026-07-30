# Architecture Decision Records (ADRs)

**1). ADR-001: Core tech-stack**

Date: 2026-07-28

Decision: Decided to standardize on the following:

1). **Web Framework:** FastAPI  
2). **Application Server:** Uvicorn  
3). **Configuration Management:** pydantic-settings  
4). **Testing Suite:** pytest + pytest-asyncio + httpx  
5). **Quality & Tooling:** ruff + pre-commit

**2). ADR-002: Package Manager Selection (uv)**

Date: 2026-07-28

Decision: Selected uv over pip/poetry.

Reason: uv provides faster package resolution, lockfile support, and clean environment isolation.

**3). ADR 003: Reordering Phase 1 Execution Sequence in roadmap**

Date: 2026-07-30

Context: Phase 1 originally scheduled the Frontend Skeleton immediately after the Backend Skeleton.

Decision: Deferring the **Frontend Skeleton** to the end of Phase 1 and prioritizing backend stability tools:

1. **Docker Environment:** Containerize the FastAPI backend and compose foundational infrastructure.
2. **Testing Infrastructure:** Configure `pytest`, `pytest-asyncio`, and `httpx` to test endpoints early.
3. **CI/CD:** Set up GitHub Actions to enforce linting (`ruff`) and test execution on Pull Requests.
4. **Frontend Skeleton:** Introduce UI components once backend capabilities exist.

Reason: Building UI components after establishing core RAG pipeline contracts prevents redundant frontend refactoring.
