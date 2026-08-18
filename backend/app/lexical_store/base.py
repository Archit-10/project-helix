from abc import ABC, abstractmethod

from app.schemas.document_chunk import DocumentChunk
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult


class LexicalStore(ABC):
    """Base interface for lexical search."""

    @abstractmethod
    def add(self, chunk: DocumentChunk) -> None:
        """Add a document chunk to the lexical index."""

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[SearchResult]:
        """Return the most relevant chunks for a query."""

    @abstractmethod
    def delete(self, document_id: str) -> None:
        """Delete all chunks belonging to a document."""
