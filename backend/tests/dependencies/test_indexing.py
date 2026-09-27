from app.dependencies.indexing import get_indexing_service
from app.dependencies.retrieval import get_retrieval_service
from app.dependencies.stores import (
    get_lexical_store,
    get_vector_store,
)
from app.services.indexing import IndexingService


def test_get_indexing_service():
    get_indexing_service.cache_clear()

    service = get_indexing_service()

    assert isinstance(service, IndexingService)


def test_get_indexing_service_is_cached():
    get_indexing_service.cache_clear()

    first = get_indexing_service()
    second = get_indexing_service()

    assert first is second


def test_indexing_and_retrieval_share_stores():
    get_indexing_service.cache_clear()
    get_retrieval_service.cache_clear()
    get_lexical_store.cache_clear()
    get_vector_store.cache_clear()

    indexing_service = get_indexing_service()
    retrieval_service = get_retrieval_service()

    assert (
        indexing_service.lexical_store
        is retrieval_service.lexical_service.lexical_store
    )
    assert (
        indexing_service.vector_store is retrieval_service.semantic_service.vector_store
    )
