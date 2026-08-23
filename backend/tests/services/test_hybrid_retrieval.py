from unittest.mock import Mock

import pytest

from app.rerankers.base import Reranker
from app.schemas.search_result import SearchResult
from app.services.hybrid_retrieval import HybridRetrievalService
from app.services.lexical_retrieval import LexicalRetrievalService
from app.services.retrieval import SemanticRetrievalService


def create_reranker():
    reranker = Mock(spec=Reranker)
    reranker.rerank.side_effect = lambda query, results, top_k: results[:top_k]
    return reranker


def test_hybrid_retrieval():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.9,
        ),
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.6,
        ),
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
        ),
        SearchResult(
            chunk_id="chunk-3",
            document_id="doc-3",
            score=0.7,
        ),
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
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


def test_hybrid_retrieval_merges_duplicate_results():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
        )
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.6,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].document_id == "doc-1"
    assert results[0].score == 0.7


def test_hybrid_retrieval_uses_custom_weights():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.8,
        )
    ]

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.4,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        semantic_weight=0.7,
        lexical_weight=0.3,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].score == pytest.approx(0.68)


def test_hybrid_retrieval_with_only_semantic_results():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    semantic_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.9,
        )
    ]

    lexical_service.search.return_value = []

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
    )

    results = service.search(
        query="authentication",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].score == pytest.approx(0.45)


def test_hybrid_retrieval_with_only_lexical_results():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    semantic_service.search.return_value = []

    lexical_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.8,
        )
    ]

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
    )

    results = service.search(
        query="Kafka",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-2"
    assert results[0].score == pytest.approx(0.4)


def test_hybrid_retrieval_invalid_top_k():
    semantic_service = Mock(spec=SemanticRetrievalService)
    lexical_service = Mock(spec=LexicalRetrievalService)
    reranker = create_reranker()

    service = HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
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

    with pytest.raises(ValueError):
        HybridRetrievalService(
            semantic_service=semantic_service,
            lexical_service=lexical_service,
            reranker=reranker,
            semantic_weight=-0.1,
            lexical_weight=1.1,
        )
