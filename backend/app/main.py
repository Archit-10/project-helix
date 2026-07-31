import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.settings import get_settings
from app.core.logging import configure_logging

settings = get_settings()

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Project Helix...")
    yield
    logger.info("Shutting down Project Helix...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    app.include_router(
        api_router,
        prefix=settings.API_V1_STR,
    )

    return app


app = create_app()
