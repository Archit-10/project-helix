from abc import ABC, abstractmethod

from app.schemas.vector_record import VectorRecord


class VectorStore(ABC):
    """Base interface for vector storage."""

    @abstractmethod
    def add(self, record: VectorRecord) -> None:
        """Add a vector record to the store."""

    @abstractmethod
    def search(
        self,
        vector: list[float],
        top_k: int,
    ) -> list[VectorRecord]:
        """Search for the most similar vectors."""

    @abstractmethod
    def delete(self, document_id: str) -> None:
        """Delete all vectors belonging to a document."""
