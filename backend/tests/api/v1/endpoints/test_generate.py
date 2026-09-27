from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.dependencies.response_generation import (
    get_response_generation_service,
)
from app.main import app
from app.schemas.citation import Citation
from app.schemas.generation_response import GenerationResponse
from app.schemas.stream_event import StreamEvent

client = TestClient(app)


def test_generate():
    response_generation_service = Mock()

    response_generation_service.generate.return_value = GenerationResponse(
        answer="Kafka uses SASL for authentication.",
        citations=[
            Citation(
                document_id="doc-1",
                chunk_id="chunk-1",
                file_name="kafka.md",
                path="/knowledge/kafka.md",
            )
        ],
    )

    app.dependency_overrides[get_response_generation_service] = lambda: (
        response_generation_service
    )

    response = client.post(
        "/api/v1/generate",
        json={
            "query": "How does Kafka authentication work?",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "Kafka uses SASL for authentication.",
        "citations": [
            {
                "document_id": "doc-1",
                "chunk_id": "chunk-1",
                "file_name": "kafka.md",
                "path": "/knowledge/kafka.md",
            }
        ],
    }

    response_generation_service.generate.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    app.dependency_overrides.clear()


def test_generate_stream():
    response_generation_service = Mock()

    response_generation_service.generate_stream.return_value = iter(
        [
            StreamEvent(
                type="token",
                content="Kafka",
            ),
            StreamEvent(
                type="token",
                content=" uses",
            ),
            StreamEvent(
                type="token",
                content=" SASL",
            ),
            StreamEvent(
                type="token",
                content=" authentication.",
            ),
            StreamEvent(
                type="citations",
                citations=[
                    Citation(
                        document_id="doc-1",
                        chunk_id="chunk-1",
                        file_name="kafka.md",
                        path="/knowledge/kafka.md",
                    )
                ],
            ),
            StreamEvent(type="done"),
        ]
    )

    app.dependency_overrides[get_response_generation_service] = lambda: (
        response_generation_service
    )

    response = client.post(
        "/api/v1/generate/stream",
        json={
            "query": "How does Kafka authentication work?",
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    assert response.headers["content-type"].startswith("text/event-stream")

    expected_response = (
        'data: {"type":"token","content":"Kafka","citations":null}\n\n'
        'data: {"type":"token","content":" uses","citations":null}\n\n'
        'data: {"type":"token","content":" SASL","citations":null}\n\n'
        'data: {"type":"token","content":" authentication.","citations":null}\n\n'
        'data: {"type":"citations","content":null,"citations":['
        '{"document_id":"doc-1","chunk_id":"chunk-1",'
        '"file_name":"kafka.md","path":"/knowledge/kafka.md"}'
        "]}\n\n"
        'data: {"type":"done","content":null,"citations":null}\n\n'
    )

    assert response.text == expected_response

    response_generation_service.generate_stream.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    app.dependency_overrides.clear()
