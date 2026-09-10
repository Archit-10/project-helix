import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.metrics import (
    http_request_duration_seconds,
    http_requests_total,
    http_responses_total,
)
from app.middleware.http_logging import HTTPLoggingMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(HTTPLoggingMiddleware)

    @app.get("/test")
    def test_endpoint():
        return {"message": "success"}

    @app.get("/error")
    def error_endpoint():
        raise ValueError("Test error")

    return app


def test_http_request_and_response_are_logged(caplog):
    app = create_app()
    client = TestClient(app)

    with caplog.at_level(logging.INFO):
        response = client.get("/test")

    assert response.status_code == 200

    messages = [record.message for record in caplog.records]

    assert "HTTP request" in messages
    assert "HTTP response" in messages

    response_record = next(
        record for record in caplog.records if record.message == "HTTP response"
    )

    assert response_record.http_method == "GET"
    assert response_record.http_path == "/test"
    assert response_record.status_code == 200
    assert response_record.duration_ms >= 0


def test_http_request_failure_is_logged(caplog):
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    with caplog.at_level(logging.INFO):
        response = client.get("/error")

    assert response.status_code == 500

    failure_record = next(
        record for record in caplog.records if record.message == "HTTP request failed"
    )

    assert failure_record.http_method == "GET"
    assert failure_record.http_path == "/error"
    assert failure_record.duration_ms >= 0
    assert failure_record.exc_info is not None
    assert failure_record.exc_info[0] is ValueError
    assert str(failure_record.exc_info[1]) == "Test error"


def test_http_request_metrics_are_recorded():
    app = create_app()
    client = TestClient(app)

    before_requests = http_requests_total.labels(
        method="GET",
        path="/test",
    )._value.get()

    before_responses = http_responses_total.labels(
        method="GET",
        path="/test",
        status_code="200",
    )._value.get()

    before_duration = http_request_duration_seconds.labels(
        method="GET",
        path="/test",
    )._sum.get()

    response = client.get("/test")

    assert response.status_code == 200

    after_requests = http_requests_total.labels(
        method="GET",
        path="/test",
    )._value.get()

    after_responses = http_responses_total.labels(
        method="GET",
        path="/test",
        status_code="200",
    )._value.get()

    after_duration = http_request_duration_seconds.labels(
        method="GET",
        path="/test",
    )._sum.get()

    assert after_requests == before_requests + 1
    assert after_responses == before_responses + 1
    assert after_duration > before_duration


def test_http_request_duration_is_recorded_on_failure():
    app = create_app()
    client = TestClient(app, raise_server_exceptions=False)

    before_duration = http_request_duration_seconds.labels(
        method="GET",
        path="/error",
    )._sum.get()

    response = client.get("/error")

    assert response.status_code == 500

    after_duration = http_request_duration_seconds.labels(
        method="GET",
        path="/error",
    )._sum.get()

    assert after_duration > before_duration
