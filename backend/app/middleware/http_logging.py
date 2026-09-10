import logging
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.metrics import (
    http_request_duration_seconds,
    http_requests_total,
    http_responses_total,
)

logger = logging.getLogger(__name__)


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests and outgoing responses."""

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        start_time = perf_counter()

        method = request.method
        path = request.url.path

        http_requests_total.labels(
            method=method,
            path=path,
        ).inc()

        logger.info(
            "HTTP request",
            extra={
                "http_method": method,
                "http_path": path,
            },
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_seconds = perf_counter() - start_time

            http_request_duration_seconds.labels(
                method=method,
                path=path,
            ).observe(duration_seconds)

            logger.exception(
                "HTTP request failed",
                extra={
                    "http_method": method,
                    "http_path": path,
                    "duration_ms": round(
                        duration_seconds * 1000,
                        2,
                    ),
                },
            )

            raise

        duration_seconds = perf_counter() - start_time

        http_request_duration_seconds.labels(
            method=method,
            path=path,
        ).observe(duration_seconds)

        http_responses_total.labels(
            method=method,
            path=path,
            status_code=str(response.status_code),
        ).inc()

        logger.info(
            "HTTP response",
            extra={
                "http_method": method,
                "http_path": path,
                "status_code": response.status_code,
                "duration_ms": round(
                    duration_seconds * 1000,
                    2,
                ),
            },
        )

        return response
