from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

router = APIRouter()


@router.get("/metrics")
def metrics() -> Response:
    """Returns application metrics in Prometheus format."""

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
