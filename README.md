# Project Helix

**Enterprise Engineering Knowledge Platform powered by Hybrid Retrieval-Augmented Generation (RAG)**

Project Helix is a production-oriented engineering knowledge platform designed to retrieve, evaluate, and generate citation-backed answers from technical documentation.

It combines **keyword retrieval, semantic vector search, reranking, caching, evaluation, authentication, authorization, and observability** into a modular backend system.

> **Status:** Actively developed

## Why Helix?

Engineering organizations spread knowledge across API documentation, design documents, incident reports, meeting notes, repositories, and operational documentation.

Traditional keyword search can miss semantically related information, while standalone LLMs can generate answers that are difficult to verify.

Helix combines both approaches:

```text
Engineering Documents
        │
        ▼
Document Ingestion
        │
        ▼
Normalization
        │
        ▼
Chunking + Metadata
        │
        ├───────────────┐
        ▼               ▼
   BM25 Index      Vector Index
        │               │
        └───────┬───────┘
                ▼
        Hybrid Retrieval
                │
                ▼
            Reranking
                │
                ▼
        Relevant Context
                │
                ▼
          LLM Generation
                │
                ▼
       Answer + Citations
```

The goal is not simply to generate an answer, but to provide an answer that can be **traced back to the underlying engineering knowledge**.

## Key Features

### Hybrid Retrieval

Helix combines two complementary retrieval strategies:

* **BM25 keyword retrieval** for exact terminology, identifiers, API paths, configuration names, and error messages.
* **Vector retrieval** for semantic similarity and concept-level matching.
* Hybrid candidate combination improves coverage across both lexical and semantic queries.
* Metadata filtering restricts retrieval to relevant subsets of the knowledge base.

### Retrieval Evaluation

The retrieval pipeline includes evaluation capabilities for measuring search quality.

Current evaluation metrics include:

* Recall@K
* Precision@K
* Mean Reciprocal Rank (MRR)
* Citation precision
* Answer exact match

Evaluation cases can contain expected chunks, retrieved results, cited chunks, generated answers, and expected answers.

### Citation-Backed Generation

Retrieved chunks retain their source metadata throughout the pipeline.

Generated answers can therefore be associated with the evidence used to produce them, making responses easier to verify and audit.

### Caching

Helix includes an application-level caching layer for expensive retrieval operations.

The cache:

* Uses deterministic request keys.
* Supports TTL-based expiration.
* Includes query, result count, and metadata filters in retrieval keys.
* Is invalidated after successful knowledge-base indexing.
* Exposes cache hit/miss Prometheus metrics.

### Authentication & Authorization

The API includes authentication and authorization controls for protected operations.

Authorization follows role-based access control (RBAC), allowing different permissions to be applied to different users and operations.

### Observability

Helix includes application observability through:

* Structured logging
* Request/response logging
* Prometheus metrics
* Cache hit/miss metrics
* Retrieval and indexing metrics

The architecture is designed so that system behavior can be investigated rather than treated as a black box.

### Modular Document Ingestion

Documents are normalized into a common representation before entering the indexing pipeline.

The indexing flow is designed around:

```text
Document
   ↓
Normalization
   ↓
Chunking
   ↓
Metadata Extraction
   ↓
Embedding Generation
   ↓
Vector Index
   +
Keyword Index
```

This keeps document parsing and retrieval concerns separated.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │   Engineering Docs  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Ingestion Layer    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Normalization       │
                         │ + Chunking          │
                         │ + Metadata          │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
              ┌─────────────────┐      ┌─────────────────┐
              │  Keyword Index  │      │   Vector Index  │
              │      BM25       │      │      FAISS      │
              └────────┬────────┘      └────────┬────────┘
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ Hybrid Retrieval    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Reranking           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Context Assembly    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ LLM Generation      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Answer + Citations  │
                         └─────────────────────┘
```

Cross-cutting infrastructure provides:

```text
Authentication
Authorization
Caching
Logging
Metrics
Evaluation
```

## Tech Stack

| Area               | Technology                        |
| ------------------ | --------------------------------- |
| Language           | Python 3.12                       |
| API                | FastAPI                           |
| Package Management | uv                                |
| Vector Search      | FAISS                             |
| Keyword Search     | BM25                              |
| Embeddings         | Sentence Transformers             |
| LLM                | Local / configurable LLM provider |
| Validation         | Pydantic                          |
| Testing            | pytest                            |
| Linting            | Ruff                              |
| Metrics            | Prometheus                        |
| Containerization   | Docker                            |
| CI                 | GitHub Actions                    |

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   ├── core/
│   ├── evaluation/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── demo-knowledge/
├── tests/
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

The application is organized into separate API, service, core infrastructure, evaluation, schema, and model layers to keep responsibilities isolated.


## Getting Started

### Prerequisites

* Python 3.12+
* `uv`
* Git
* Docker *(optional)*

Clone the repository:

```bash
git clone https://github.com/Archit-10/project-helix.git
cd project-helix/backend
```

Install dependencies:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

Start the FastAPI application:

```bash
uv run uvicorn app.main:app --reload
```

The API will be available locally at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

## Development

Helix follows an incremental engineering workflow with automated testing and linting.

Before committing changes:

```bash
uv run pytest
uv run ruff check .
```

The project uses feature branches for isolated development and integrates completed work into the `dev` branch.

---

## Evaluation

Helix treats retrieval and generation as measurable system components rather than relying only on subjective answer quality.

An evaluation case can contain:

```text
Query
  │
  ├── Expected chunks
  ├── Retrieved chunks
  ├── Cited chunks
  ├── Generated answer
  └── Expected answer
```

This allows retrieval quality, citation quality, and answer quality to be evaluated independently.

## Design Principles

### Grounded over Generative

The system prioritizes retrieved engineering evidence over unsupported model-generated knowledge.

### Modular Components

Ingestion, retrieval, ranking, generation, caching, and evaluation are separated so individual components can evolve independently.

### Measurable Retrieval

Retrieval quality is evaluated using explicit metrics rather than relying only on generated responses.

### Observable Systems

Important application behavior is exposed through logs and metrics to make failures and performance issues easier to investigate.

### Failure-Aware Design

Caches and external model dependencies are treated as infrastructure components rather than sources of truth.

Failures should be explicit instead of silently producing unreliable results.

---

## Current Status

In progress:

* [ ] Public demo
* [ ] Hosted deployment
* [ ] Demo frontend
* [ ] Production-oriented LLM provider integration

## License

This project is currently intended as a personal engineering and portfolio project.
