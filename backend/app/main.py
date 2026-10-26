import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config.settings import get_settings
from app.core.logging import configure_logging
from app.dependencies.indexing import get_indexing_service
from app.dependencies.ingestion import get_ingestion_service
from app.middleware.http_logging import HTTPLoggingMiddleware

settings = get_settings()

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Project Helix...")

    if settings.DEMO_MODE:
        demo_dir = Path(__file__).resolve().parents[1] / "demo-knowledge"

        if not demo_dir.is_dir():
            raise RuntimeError(f"Demo knowledge directory not found: {demo_dir}")

        documents = sorted(demo_dir.glob("*.md"))

        if not documents:
            raise RuntimeError(f"No Markdown documents found in: {demo_dir}")

        ingestion_service = get_ingestion_service()
        indexing_service = get_indexing_service()

        logger.info("Indexing %d demo documents...", len(documents))

        for path in documents:
            document = ingestion_service.ingest(path)
            chunks, _ = indexing_service.index(document)

            logger.info(
                "Indexed demo document %s (%d chunks)",
                path.name,
                len(chunks),
            )

        logger.info("Demo knowledge base initialized.")

    yield

    logger.info("Shutting down Project Helix...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    app.add_middleware(HTTPLoggingMiddleware)

    app.include_router(
        api_router,
        prefix=settings.API_V1_STR,
    )

    return app


app = create_app()
