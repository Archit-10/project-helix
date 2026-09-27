from unittest.mock import Mock

import pytest

from app.core.cache_memory import InMemoryCache
from app.rerankers.base import Reranker
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult
from app.services.hybrid_retrieval import HybridRetrievalService
from app.services.lexical_retrieval import LexicalRetrievalService
from app.services.retrieval import SemanticRetrievalService


def create_reranker():
    reranker = Mock(spec=Reranker)
    reranker.rerank.side_effect = lambda query, results, top_k: results[:top_k]
    return reranker


def create_cache():
    return InMemoryCache()


def test_hybrid_retrieval(metadata: DocumentMetadata):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.9,
            content="Kafka authentication content.",
            metadata=metadata,
        ),
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.6,
            content="Security policy content.",
            metadata=metadata,
        ),
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
            content="Kafka authentication content.",
            metadata=metadata,
        ),
        SearchResult(
            chunk_id="chunk-3",
            document_id="doc-3",
            score=0.7,
            content="Kafka configuration content.",
            metadata=metadata,
        ),
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="Kafka authentication",
        top_k=3,
    )

    assert len(results) == 3
    assert results[0].chunk_id == "chunk-1"
    assert results[0].document_id == "doc-1"

    semantic_service.search.assert_called_once_with(
        query="Kafka authentication",
        top_k=3,
        metadata_filter=None,
    )

    lexical_service.search.assert_called_once_with(
        query="Kafka authentication",
        top_k=3,
        metadata_filter=None,
    )

    reranker.rerank.assert_called_once_with(
        query="Kafka authentication",
        results=results,
        top_k=3,
    )


def test_hybrid_retrieval_merges_duplicate_results(metadata: DocumentMetadata):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.6,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].document_id == "doc-1"
    assert results[0].score == 0.7
    assert results[0].content == "Kafka authentication content."
    assert results[0].metadata == metadata


def test_hybrid_retrieval_uses_custom_weights(metadata: DocumentMetadata):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.4,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
        semantic_weight=0.7,
        lexical_weight=0.3,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].score == pytest.approx(0.68)
    assert results[0].content == "Kafka authentication content."
    assert results[0].metadata == metadata


def test_hybrid_retrieval_with_only_semantic_results(
    metadata: DocumentMetadata,
):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.9,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="authentication",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].score == pytest.approx(0.45)
    assert results[0].content == "Kafka authentication content."
    assert results[0].metadata == metadata


def test_hybrid_retrieval_with_only_lexical_results(
    metadata: DocumentMetadata,
):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    semantic_service.search.return_value = []

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.8,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-2"
    assert results[0].score == pytest.approx(0.4)
    assert results[0].content == "Kafka authentication content."
    assert results[0].metadata == metadata


def test_hybrid_retrieval_invalid_top_k():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        service.search(
            query="Kafka",
            top_k=0,
        )


def test_hybrid_retrieval_invalid_weights():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    with pytest.raises(ValueError):
        HybridRetrievalService(
            semantic_service=semantic_service,
            lexical_service=lexical_service,
            reranker=reranker,
            cache=cache,
            semantic_weight=-0.1,
            lexical_weight=1.1,
        )


def test_hybrid_retrieval_uses_cached_results(metadata: DocumentMetadata):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = InMemoryCache()

    cached_result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=0.9,
        content="Cached content.",
        metadata=metadata,
    )

    cache.set(
        "retrieval:Kafka:5:None",
        [cached_result],
    )

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert results == [cached_result]
    semantic_service.search.assert_not_called()
    lexical_service.search.assert_not_called()
    reranker.rerank.assert_not_called()


def test_hybrid_retrieval_caches_new_results(metadata: DocumentMetadata):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = InMemoryCache()

    semantic_result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=0.9,
        content="Kafka content.",
        metadata=metadata,
    )

    semantic_service.search.return_value = [semantic_result]
    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].document_id == "doc-1"
    assert results[0].score == pytest.approx(0.45)
    assert results[0].content == "Kafka content."
    assert results[0].metadata == metadata

    cached_results = cache.get(
        "retrieval:Kafka:5:None",
    )

    assert cached_results == results


def test_hybrid_retrieval_cache_isolated_by_top_k(
    metadata: DocumentMetadata,
):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=0.9,
        content="Kafka content.",
        metadata=metadata,
    )

    semantic_service.search.return_value = [result]
    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    service.search(
        query="Kafka",
        top_k=5,
    )

    service.search(
        query="Kafka",
        top_k=10,
    )

    assert semantic_service.search.call_count == 2
    assert lexical_service.search.call_count == 2


def test_hybrid_retrieval_cache_isolated_by_query(
    metadata: DocumentMetadata,
):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=0.9,
        content="Kafka content.",
        metadata=metadata,
    )

    semantic_service.search.return_value = [result]
    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    service.search(
        query="Kafka",
        top_k=5,
    )

    service.search(
        query="Redis",
        top_k=5,
    )

    assert semantic_service.search.call_count == 2
    assert lexical_service.search.call_count == 2


def test_hybrid_retrieval_cache_isolated_by_metadata_filter(
    metadata: DocumentMetadata,
):
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()
    cache = create_cache()

    result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=0.9,
        content="Kafka content.",
        metadata=metadata,
    )

    semantic_service.search.return_value = [result]
    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )

    filter_one = MetadataFilter(
        file_name="kafka.md",
    )

    filter_two = MetadataFilter(
        file_name="redis.md",
    )

    service.search(
        query="Kafka",
        top_k=5,
        metadata_filter=filter_one,
    )

    service.search(
        query="Kafka",
        top_k=5,
        metadata_filter=filter_two,
    )

    assert semantic_service.search.call_count == 2
    assert lexical_service.search.call_count == 2
