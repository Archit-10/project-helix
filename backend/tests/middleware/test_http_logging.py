import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

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
