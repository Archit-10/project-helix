from pathlib import Path

from app.providers.base import DocumentProvider
from app.schemas.normalized_document import NormalizedDocument


class IngestionService:
    """Coordinates document ingestion using registered providers."""

    def __init__(self, providers: list[DocumentProvider]):
        self.providers = providers

    def ingest(self, path: Path) -> NormalizedDocument:
        for provider in self.providers:
            if provider.supports(path):
                return provider.load(path)

        raise ValueError(f"No provider found for file: {path}")
