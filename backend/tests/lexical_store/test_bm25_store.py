from datetime import datetime
from pathlib import Path

import pytest

from app.lexical_store.bm25_store import BM25Store
from app.schemas.document_chunk import DocumentChunk
from app.schemas.document_metadata import DocumentMetadata


def create_chunk(
    document_id: str,
    chunk_id: str,
    content: str,
) -> DocumentChunk:
    return DocumentChunk(
        document_id=document_id,
        chunk_id=chunk_id,
        chunk_index=0,
        content=content,
        metadata=DocumentMetadata(
            file_name="sample.txt",
            extension=".txt",
            path=Path("sample_documents/sample.txt"),
            size_bytes=100,
            last_modified=datetime.now(),
            content_hash="dummy-hash",
        ),
    )


def test_bm25_search():
    store = BM25Store()

    store.add(
        create_chunk(
            "doc-1",
            "chunk-1",
            "Kafka processes authentication events",
        )
    )

    store.add(
        create_chunk(
            "doc-2",
            "chunk-2",
            "Redis stores cached session data",
        )
    )

    results = store.search(
        query="Kafka authentication",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"


def test_empty_store_returns_empty_results():
    store = BM25Store()

    results = store.search(
        query="Kafka",
        top_k=5,
    )

    assert results == []


def test_invalid_top_k():
    store = BM25Store()

    with pytest.raises(
        ValueError,
        match="top_k must be greater than 0",
    ):
        store.search(
            query="Kafka",
            top_k=0,
        )


def test_delete_document():
    store = BM25Store()

    store.add(
        create_chunk(
            "doc-1",
            "chunk-1",
            "Kafka authentication",
        )
    )

    store.add(
        create_chunk(
            "doc-2",
            "chunk-2",
            "Redis caching",
        )
    )

    store.delete("doc-1")

    results = store.search(
        query="Kafka",
        top_k=5,
    )

    assert results == []


def test_delete_all_documents():
    store = BM25Store()

    store.add(
        create_chunk(
            "doc-1",
            "chunk-1",
            "Kafka authentication",
        )
    )

    store.delete("doc-1")

    assert store.chunks == []
    assert store.index is None


def test_top_k_limits_results():
    store = BM25Store()

    store.add(
        create_chunk(
            "doc-1",
            "chunk-1",
            "Kafka authentication events",
        )
    )

    store.add(
        create_chunk(
            "doc-2",
            "chunk-2",
            "Kafka authentication service",
        )
    )

    results = store.search(
        query="Kafka authentication",
        top_k=1,
    )

    assert len(results) == 1
