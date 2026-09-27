from fastapi.testclient import TestClient

from app.main import create_app


def test_http_metrics_are_exposed_by_metrics_endpoint():
    app = create_app()
    client = TestClient(app)

    health_response = client.get("/api/v1/health")

    assert health_response.status_code == 200

    metrics_response = client.get("/api/v1/metrics")

    assert metrics_response.status_code == 200

    body = metrics_response.text

    assert 'http_requests_total{method="GET",path="/api/v1/health"}' in body
    assert (
        'http_responses_total{method="GET",path="/api/v1/health",status_code="200"}'
        in body
    )
    assert (
        'http_request_duration_seconds_count{method="GET",path="/api/v1/health"}'
        in body
    )
