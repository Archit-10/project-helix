import json
import logging
import sys

from app.core.logging import JSONFormatter


def test_json_formatter():
    formatter = JSONFormatter()

    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    result = formatter.format(record)

    log_entry = json.loads(result)

    assert log_entry["level"] == "INFO"
    assert log_entry["logger"] == "test.logger"
    assert log_entry["message"] == "Test message"
    assert "timestamp" in log_entry


def test_json_formatter_includes_exception():
    formatter = JSONFormatter()

    try:
        raise ValueError("Test error")
    except ValueError:
        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="test.logger",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg="Something went wrong",
        args=(),
        exc_info=exc_info,
    )

    result = formatter.format(record)

    log_entry = json.loads(result)

    assert log_entry["level"] == "ERROR"
    assert log_entry["logger"] == "test.logger"
    assert log_entry["message"] == "Something went wrong"
    assert "exception" in log_entry
    assert "ValueError: Test error" in log_entry["exception"]


def test_json_formatter_includes_context():
    formatter = JSONFormatter()

    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="HTTP response",
        args=(),
        exc_info=None,
    )

    record.http_method = "GET"
    record.http_path = "/test"
    record.status_code = 200
    record.duration_ms = 12.34

    result = formatter.format(record)

    log_entry = json.loads(result)

    assert log_entry["context"]["http_method"] == "GET"
    assert log_entry["context"]["http_path"] == "/test"
    assert log_entry["context"]["status_code"] == 200
    assert log_entry["context"]["duration_ms"] == 12.34
