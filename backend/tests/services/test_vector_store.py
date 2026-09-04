from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

from app.schemas.document_metadata import DocumentMetadata
from app.schemas.vector_record import VectorRecord
from app.services.vector_store import VectorStoreService


def create_metadata() -> DocumentMetadata:
    return DocumentMetadata(
        file_name="sample.txt",
        extension=".txt",
        path=Path("sample_documents/sample.txt"),
        size_bytes=100,
        last_modified=datetime.now(),
        content_hash="dummy-hash",
    )


def test_vector_store_service():
    store = MagicMock()

    record = VectorRecord(
        chunk_id="chunk-1",
        document_id="doc-1",
        vector=[0.1, 0.2, 0.3],
        metadata=create_metadata(),
        content="test content",
    )

    store.search.return_value = [record]

    service = VectorStoreService(store)

    service.add(record)

    results = service.search(
        vector=[0.1, 0.2, 0.3],
        top_k=5,
    )

    service.delete("doc-1")

    store.add.assert_called_once_with(record)

    store.search.assert_called_once_with(
        [0.1, 0.2, 0.3],
        5,
    )

    store.delete.assert_called_once_with("doc-1")

    assert results == [record]
