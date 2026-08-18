from abc import ABC, abstractmethod

from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding


class EmbeddingProvider(ABC):
    """Base interface for embedding providers."""

    @abstractmethod
    def embed(
        self,
        chunk: DocumentChunk,
    ) -> Embedding:
        """Generate an embedding for a document chunk."""

    @abstractmethod
    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """Generate an embedding for arbitrary text."""
