# Retrieval Service

The Helix Engineering Platform uses a hybrid retrieval pipeline to find relevant engineering knowledge from the indexed document collection.

## Retrieval Pipeline

A search request passes through the following stages:

1. Query validation
2. Query normalization
3. Candidate retrieval
4. Hybrid score combination
5. Result ranking
6. Top-k selection
7. Citation generation

The retrieval service returns document chunks together with metadata that identifies their source.

## Keyword Retrieval

The keyword retrieval component uses BM25 to identify documents containing terms that match the user's query.

BM25 is effective for exact terminology, identifiers, configuration names, API paths, metric names, and other terms where lexical matching is important.

For example, a query containing `cache_hits_total` should strongly favor chunks containing that exact metric name.

## Vector Retrieval

The vector retrieval component converts document chunks and the incoming query into embedding vectors.

Semantic similarity is then used to identify chunks that discuss concepts related to the query even when the exact words differ.

Vector retrieval is useful when a user asks a conceptual question using terminology that differs from the source documents.

## Hybrid Retrieval

Keyword and vector retrieval provide complementary signals.

The hybrid retriever combines candidates from both retrieval methods before ranking the final results.

This allows the system to benefit from both exact lexical matching and semantic similarity.

For example, a query about "requests waiting to be processed by Kafka consumers" can retrieve documentation discussing Kafka consumer lag even if the query does not contain the exact phrase used in the source document.

## Result Ranking

Retrieved candidates are ranked using their combined relevance score.

The final ranking prioritizes chunks that provide the strongest evidence for the query.

The number of returned results is controlled by the `top_k` parameter.

Returning too few results can omit important evidence, while returning too many results can introduce irrelevant context.

## Metadata Filtering

Retrieval results can be filtered using document metadata.

Supported metadata may include:

- document identifier
- source type
- service
- application
- document section

Metadata filters are applied during retrieval so that irrelevant documents are excluded from the candidate set.

## Citations

Every retrieved chunk retains its source metadata.

The answer generation layer uses this metadata to associate statements with the source chunks that support them.

Citations allow users to inspect where an answer originated and make the generated response easier to verify.

## Retrieval Cache

Repeated retrieval requests can be served from the application cache.

The cache key includes the normalized query, requested result count, and applicable metadata filters.

Cached retrieval results are invalidated after successful knowledge-
