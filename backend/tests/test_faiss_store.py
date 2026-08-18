import pytest

from app.schemas.vector_record import VectorRecord
from app.vector_store.faiss_store import FAISSVectorStore


def test_search_empty_store():
    store = FAISSVectorStore(dimension=3)

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=5,
    )

    assert results == []


def test_add_and_search():
    store = FAISSVectorStore(dimension=3)

    record = VectorRecord(
        chunk_id="chunk-1",
        document_id="doc-1",
        vector=[1.0, 0.0, 0.0],
    )

    store.add(record)

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"
    assert results[0].score == pytest.approx(1.0)


def test_search_returns_most_similar():
    store = FAISSVectorStore(dimension=3)

    store.add(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[1.0, 0.0, 0.0],
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-1",
            vector=[0.0, 1.0, 0.0],
        )
    )

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert results[0].chunk_id == "chunk-1"


def test_delete_document():
    store = FAISSVectorStore(dimension=3)

    store.add(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[1.0, 0.0, 0.0],
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-2",
            vector=[0.0, 1.0, 0.0],
        )
    )

    store.delete("doc-1")

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=5,
    )

    assert all(result.document_id != "doc-1" for result in results)


def test_search_invalid_top_k():
    store = FAISSVectorStore(dimension=3)

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        store.search(
            vector=[1.0, 0.0, 0.0],
            top_k=0,
        )
