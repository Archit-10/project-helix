from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints.metrics import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    return app


def test_metrics_endpoint_returns_prometheus_data():
    app = create_app()
    client = TestClient(app)

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]

    body = response.text

    assert "http_requests_total" in body
    assert "http_responses_total" in body
    assert "http_request_duration_seconds" in body
