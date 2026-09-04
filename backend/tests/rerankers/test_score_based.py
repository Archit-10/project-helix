import pytest

from app.rerankers.score_based import ScoreBasedReranker
from app.schemas.search_result import SearchResult


def test_score_based_reranker_sorts_by_score():
    reranker = ScoreBasedReranker()

    results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.4,
            content="Kafka authentication content one.",
        ),
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.9,
            content="Kafka authentication content two.",
        ),
        SearchResult(
            chunk_id="chunk-3",
            document_id="doc-3",
            score=0.6,
            content="Kafka authentication content three.",
        ),
    ]

    actual = reranker.rerank(
        query="Kafka authentication",
        results=results,
        top_k=3,
    )

    assert [result.chunk_id for result in actual] == [
        "chunk-2",
        "chunk-3",
        "chunk-1",
    ]


def test_score_based_reranker_limits_top_k():
    reranker = ScoreBasedReranker()

    results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.4,
            content="Kafka authentication content one.",
        ),
        SearchResult(
            chunk_id="chunk-2",
            document_id="doc-2",
            score=0.9,
            content="Kafka authentication content two.",
        ),
        SearchResult(
            chunk_id="chunk-3",
            document_id="doc-3",
            score=0.6,
            content="Kafka authentication content three.",
        ),
    ]

    actual = reranker.rerank(
        query="Kafka",
        results=results,
        top_k=2,
    )

    assert len(actual) == 2

    assert [result.chunk_id for result in actual] == [
        "chunk-2",
        "chunk-3",
    ]


def test_score_based_reranker_rejects_invalid_top_k():
    reranker = ScoreBasedReranker()

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        reranker.rerank(
            query="Kafka",
            results=[],
            top_k=0,
        )


def test_score_based_reranker_with_empty_results():
    reranker = ScoreBasedReranker()

    actual = reranker.rerank(
        query="Kafka",
        results=[],
        top_k=5,
    )

    assert actual == []
