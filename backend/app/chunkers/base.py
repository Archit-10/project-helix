from abc import ABC, abstractmethod

from app.schemas.document_chunk import DocumentChunk
from app.schemas.normalized_document import NormalizedDocument


class Chunker(ABC):
    """Base class for all chunking strategies."""

    @abstractmethod
    def chunk(
        self,
        document: NormalizedDocument,
    ) -> list[DocumentChunk]:
        """Split a normalized document into chunks."""
