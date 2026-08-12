from unittest.mock import MagicMock

from app.schemas.vector_record import VectorRecord
from app.services.vector_store import VectorStoreService


def test_vector_store_service():
    store = MagicMock()

    record = VectorRecord(
        chunk_id="chunk-1",
        document_id="doc-1",
        vector=[0.1, 0.2, 0.3],
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
