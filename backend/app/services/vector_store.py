from app.schemas.vector_record import VectorRecord
from app.vector_store.base import VectorStore


class VectorStoreService:
    """Coordinates vector storage and retrieval."""

    def __init__(self, store: VectorStore) -> None:
        self.store = store

    def add(self, record: VectorRecord) -> None:
        self.store.add(record)

    def search(
        self,
        vector: list[float],
        top_k: int,
    ) -> list[VectorRecord]:
        return self.store.search(vector, top_k)

    def delete(self, document_id: str) -> None:
        self.store.delete(document_id)
