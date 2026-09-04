from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.dependencies.response_generation import (
    get_response_generation_service,
)
from app.main import app

client = TestClient(app)


def test_generate():
    response_generation_service = Mock()

    response_generation_service.generate.return_value = (
        "Kafka uses SASL for authentication."
    )

    app.dependency_overrides[get_response_generation_service] = (
        lambda: response_generation_service
    )

    response = client.post(
        "/api/v1/generate",
        json={
            "query": "How does Kafka authentication work?",
            "top_k": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Kafka uses SASL for authentication."}

    response_generation_service.generate.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    app.dependency_overrides.clear()
