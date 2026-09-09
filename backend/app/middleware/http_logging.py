import logging
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming HTTP requests and outgoing responses."""

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        start_time = perf_counter()

        logger.info(
            "HTTP request",
            extra={
                "http_method": request.method,
                "http_path": request.url.path,
            },
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter() - start_time) * 1000

            logger.exception(
                "HTTP request failed",
                extra={
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                },
            )

            raise

        duration_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "HTTP response",
            extra={
                "http_method": request.method,
                "http_path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            },
        )

        return response
