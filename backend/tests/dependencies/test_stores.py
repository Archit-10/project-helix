from app.dependencies.stores import (
    get_lexical_store,
    get_vector_store,
)
from app.lexical_store.bm25_store import BM25Store
from app.vector_store.faiss_store import FAISSVectorStore


def test_get_vector_store():
    get_vector_store.cache_clear()

    store = get_vector_store()

    assert isinstance(store, FAISSVectorStore)
    assert store.dimension == 384


def test_get_vector_store_is_cached():
    get_vector_store.cache_clear()

    first = get_vector_store()
    second = get_vector_store()

    assert first is second


def test_get_lexical_store():
    get_lexical_store.cache_clear()

    store = get_lexical_store()

    assert isinstance(store, BM25Store)


def test_get_lexical_store_is_cached():
    get_lexical_store.cache_clear()

    first = get_lexical_store()
    second = get_lexical_store()

    assert first is second
