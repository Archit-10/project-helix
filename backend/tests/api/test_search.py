from unittest.mock import Mock

from app.dependencies.retrieval import get_retrieval_service
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult


def test_search_endpoint(client):
    retrieval_service = Mock()

    retrieval_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.95,
            content="Kafka authentication content.",
        )
    ]

    client.app.dependency_overrides[get_retrieval_service] = lambda: retrieval_service

    response = client.post(
        "/api/v1/search",
        json={
            "query": "Kafka authentication",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "score": 0.95,
            "content": "Kafka authentication content.",
        }
    ]

    retrieval_service.search.assert_called_once_with(
        query="Kafka authentication",
        top_k=5,
        metadata_filter=None,
    )

    client.app.dependency_overrides.clear()


def test_search_rejects_empty_query(client):
    response = client.post(
        "/api/v1/search",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422


def test_search_rejects_invalid_top_k(client):
    response = client.post(
        "/api/v1/search",
        json={
            "query": "Kafka",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


def test_search_with_metadata_filter(client):
    retrieval_service = Mock()

    retrieval_service.search.return_value = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.91,
            content="Kafka authentication content.",
        )
    ]

    client.app.dependency_overrides[get_retrieval_service] = lambda: retrieval_service

    response = client.post(
        "/api/v1/search",
        json={
            "query": "Kafka authentication",
            "top_k": 5,
            "metadata_filter": {
                "extension": ".md",
            },
        },
    )

    assert response.status_code == 200

    assert response.json() == [
        {
            "chunk_id": "chunk-1",
            "document_id": "doc-1",
            "score": 0.91,
            "content": "Kafka authentication content.",
        }
    ]

    retrieval_service.search.assert_called_once_with(
        query="Kafka authentication",
        top_k=5,
        metadata_filter=MetadataFilter(
            extension=".md",
        ),
    )

    client.app.dependency_overrides.clear()
