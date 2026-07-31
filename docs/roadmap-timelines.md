# Development Roadmap & Timelines

**Phase 1 - Core Setup**

Repository Setup  
Architecture Documentation  
Backend Skeleton  
Docker Environment  
Testing Infrastructure  
CI/CD

**Implementation Note:** The frontend is intentionally scheduled after the core backend capabilities (ingestion, indexing, retrieval etc.). This will allow the UI to be built against stable APIs and keeps early development focused on the platform's core functionality.

**Phase 2 - Knowledge Ingestion**

Local File Connector  
Parsing of knowledge sources  
Metadata Extraction  
Chunking

**Phase 3 - Indexing**

Embedding Pipeline  
Vector Database  
Lexical Index  
Incremental Indexing

**Phase 4 - Retrieval**

Semantic Search  
BM25 Search  
Hybrid Retrieval  
Metadata Filtering  
Reranking

**Phase 5 - Response Generation**

Prompt Builder  
Local LLM Integration  
Citation Generation  
Streaming Responses

**Phase 6 - Platform**

Authentication  
Observability  
Caching  
Evaluation Framework
