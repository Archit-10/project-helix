from fastapi import APIRouter

from app.api.v1.endpoints import generate, health, index, search, version

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"],
)
api_router.include_router(
    version.router,
    tags=["System"],
)
api_router.include_router(
    search.router,
    tags=["Search"],
)
api_router.include_router(
    index.router,
    tags=["Indexing"],
)
api_router.include_router(
    generate.router,
    tags=["Generation"],
)
