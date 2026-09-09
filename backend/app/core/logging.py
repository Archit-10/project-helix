import json
import logging
import sys
from datetime import UTC, datetime


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        standard_fields = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "taskName",
        }

        context = {
            key: value
            for key, value in record.__dict__.items()
            if key not in standard_fields
        }

        if context:
            log_entry["context"] = context

        if record.exc_info:
            log_entry["exception"] = self.formatException(
                record.exc_info,
            )

        return json.dumps(log_entry)


def configure_logging() -> None:
    """Configures application-wide structured logging."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
    )
