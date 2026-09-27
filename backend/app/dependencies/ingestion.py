from functools import lru_cache

from app.providers.base import DocumentProvider
from app.providers.markdown import MarkdownProvider
from app.providers.pdf import PdfProvider
from app.providers.text import TextProvider
from app.services.ingestion import IngestionService


@lru_cache
def get_ingestion_service() -> IngestionService:
    providers: list[DocumentProvider] = [
        TextProvider(),
        MarkdownProvider(),
        PdfProvider(),
    ]

    return IngestionService(
        providers=providers,
    )
