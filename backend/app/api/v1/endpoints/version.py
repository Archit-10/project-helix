from fastapi import APIRouter

from app.config.settings import get_settings
from app.schemas.version import VersionResponse

router = APIRouter()

settings = get_settings()


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Application Version",
    description="Returns application version and environment information.",
)
async def get_version() -> VersionResponse:
    return VersionResponse(
        project_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENV,
    )
