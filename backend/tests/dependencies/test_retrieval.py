from app.dependencies.retrieval import get_retrieval_service
from app.services.hybrid_retrieval import HybridRetrievalService


def test_get_retrieval_service():
    get_retrieval_service.cache_clear()

    service = get_retrieval_service()

    assert isinstance(service, HybridRetrievalService)


def test_get_retrieval_service_is_cached():
    get_retrieval_service.cache_clear()

    first = get_retrieval_service()
    second = get_retrieval_service()

    assert first is second
