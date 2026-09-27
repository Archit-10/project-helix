from pathlib import Path
from unittest.mock import Mock

from app.dependencies.indexing import get_indexing_service
from app.dependencies.ingestion import get_ingestion_service
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.normalized_document import NormalizedDocument


def test_index_endpoint(client):
    ingestion_service = Mock()
    indexing_service = Mock()

    document = NormalizedDocument(
        content="Project Helix is a RAG platform.",
        metadata=DocumentMetadata(
            file_name="sample.txt",
            extension=".txt",
            path=Path("sample_documents/sample.txt"),
            size_bytes=100,
            last_modified="2026-08-20T00:00:00",
            content_hash="dummy-hash",
        ),
    )

    ingestion_service.ingest.return_value = document
    indexing_service.index.return_value = (
        ["chunk-1", "chunk-2"],
        [],
    )

    client.app.dependency_overrides[get_ingestion_service] = lambda: ingestion_service
    client.app.dependency_overrides[get_indexing_service] = lambda: indexing_service

    response = client.post(
        "/api/v1/index",
        json={
            "path": "sample_documents/sample.txt",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "document_id": "dummy-hash",
        "chunks_indexed": 2,
    }

    ingestion_service.ingest.assert_called_once_with(
        Path("sample_documents/sample.txt")
    )

    indexing_service.index.assert_called_once_with(document)

    client.app.dependency_overrides.clear()


def test_index_rejects_empty_path(client):
    response = client.post(
        "/api/v1/index",
        json={
            "path": "",
        },
    )

    assert response.status_code == 422


def test_index_rejects_missing_path(client):
    response = client.post(
        "/api/v1/index",
        json={},
    )

    assert response.status_code == 422
