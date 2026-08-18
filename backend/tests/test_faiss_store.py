from datetime import datetime
from pathlib import Path

import pytest

from app.schemas.document_metadata import DocumentMetadata
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.vector_record import VectorRecord
from app.vector_store.faiss_store import FAISSVectorStore


def create_metadata(
    file_name: str = "sample.txt",
    extension: str = ".txt",
) -> DocumentMetadata:
    return DocumentMetadata(
        file_name=file_name,
        extension=extension,
        path=Path(f"sample_documents/{file_name}"),
        size_bytes=100,
        last_modified=datetime.now(),
        content_hash=f"{file_name}-hash",
    )


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
        metadata=create_metadata(),
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
            metadata=create_metadata(),
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-1",
            vector=[0.0, 1.0, 0.0],
            metadata=create_metadata(),
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
            metadata=create_metadata(),
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-2",
            vector=[0.0, 1.0, 0.0],
            metadata=create_metadata(),
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


def test_search_with_metadata_filter():
    store = FAISSVectorStore(dimension=3)

    store.add(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[1.0, 0.0, 0.0],
            metadata=create_metadata(
                file_name="security.md",
                extension=".md",
            ),
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-2",
            vector=[0.99, 0.01, 0.0],
            metadata=create_metadata(
                file_name="architecture.txt",
                extension=".txt",
            ),
        )
    )

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=5,
        metadata_filter=MetadataFilter(
            extension=".md",
        ),
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-1"


def test_search_with_non_matching_metadata_filter():
    store = FAISSVectorStore(dimension=3)

    store.add(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[1.0, 0.0, 0.0],
            metadata=create_metadata(
                file_name="security.md",
                extension=".md",
            ),
        )
    )

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=5,
        metadata_filter=MetadataFilter(
            extension=".pdf",
        ),
    )

    assert results == []


def test_metadata_filter_is_applied_before_top_k():
    store = FAISSVectorStore(dimension=3)

    store.add(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[1.0, 0.0, 0.0],
            metadata=create_metadata(
                file_name="notes.txt",
                extension=".txt",
            ),
        )
    )

    store.add(
        VectorRecord(
            chunk_id="chunk-2",
            document_id="doc-2",
            vector=[0.9, 0.1, 0.0],
            metadata=create_metadata(
                file_name="security.md",
                extension=".md",
            ),
        )
    )

    results = store.search(
        vector=[1.0, 0.0, 0.0],
        top_k=1,
        metadata_filter=MetadataFilter(
            extension=".md",
        ),
    )

    assert len(results) == 1
    assert results[0].chunk_id == "chunk-2"
