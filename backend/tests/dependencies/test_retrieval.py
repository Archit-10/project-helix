from unittest.mock import patch

from app.dependencies.retrieval import get_retrieval_service
from app.rerankers.score_based import ScoreBasedReranker
from app.services.hybrid_retrieval import HybridRetrievalService


def test_get_retrieval_service():
    get_retrieval_service.cache_clear()

    with patch("app.dependencies.retrieval.SentenceTransformerProvider"):
        service = get_retrieval_service()

    assert isinstance(service, HybridRetrievalService)
    assert isinstance(service.reranker, ScoreBasedReranker)


def test_get_retrieval_service_is_cached():
    get_retrieval_service.cache_clear()

    with patch("app.dependencies.retrieval.SentenceTransformerProvider"):
        first = get_retrieval_service()
        second = get_retrieval_service()

    assert first is second
