# Knowledge Indexing

The Helix Engineering Platform uses an indexing pipeline to transform engineering documents into searchable knowledge.

## Indexing Pipeline

A document passes through the following stages:

1. Document ingestion
2. Content normalization
3. Chunking
4. Metadata extraction
5. Embedding generation
6. Vector index insertion
7. Keyword index insertion

The indexing pipeline produces searchable chunks that can later be retrieved by the retrieval service.

## Document Normalization

Documents can originate from different sources and formats.

The ingestion layer normalizes source content into a common document representation before indexing.

The normalized representation contains the document identifier, source information, content, and metadata.

Normalization allows downstream indexing components to operate independently of the original document format.

## Chunking

Large documents are divided into smaller chunks before indexing.

Chunking improves retrieval precision because individual search results can focus on a specific section rather than an entire document.

Chunks retain metadata linking them back to their parent document and source.

Chunk boundaries should preserve enough surrounding context for the chunk to remain understandable when retrieved independently.

## Embeddings

Each chunk is converted into an embedding vector using the configured embedding model.

The embedding represents the semantic meaning of the chunk and is stored in the vector index.

The same embedding model must be used consistently for indexed documents and incoming search queries.

## Vector Index

Embedding vectors are stored in the vector index used by the retrieval service.

The index supports nearest-neighbor search to identify chunks that are semantically similar to a query.

The vector index is rebuilt or updated when new knowledge is successfully indexed.

## Keyword Index

Chunks are also inserted into a keyword-search index.

The keyword index supports lexical retrieval for exact terms such as API paths, configuration names, metric names, error codes, and identifiers.

The keyword and vector indexes provide complementary retrieval signals.

## Metadata

Each indexed chunk retains metadata including:

- document identifier
- chunk identifier
- source type
- document title
- section
- service
- application

Metadata allows retrieval results to be filtered and enables the answer generation layer to produce citations.

## Indexing Consistency

Index updates are applied as a successful operation.

The retrieval cache is invalidated only after indexing completes successfully.

If indexing fails, the existing indexes and cached retrieval results remain unchanged.

This prevents partially indexed content from becoming visible as the active knowledge base.

## Reindexing

A full reindex processes the complete document collection and rebuilds the searchable indexes.

Full reindexing may be required when the embedding model, chunking strategy, or index configuration changes.

Incremental indexing can be used when only a subset of documents has changed.

## Operational Metrics

The indexing pipeline records metrics such as:

- documents processed
- chunks created
- embedding generation latency
- indexing duration
- indexing failures

These metrics help operators identify bottlenecks and monitor the health of the knowledge ingestion pipeline.
