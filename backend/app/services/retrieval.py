from app.schemas.search_result import SearchResult
from app.services.embedding import EmbeddingService
from app.vector_store.base import VectorStore


class SemanticRetrievalService:
    """Retrieves relevant chunks using semantic similarity."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int,
    ) -> list[SearchResult]:
        query_vector = self.embedding_service.embed_text(query)

        return self.vector_store.search(
            vector=query_vector,
            top_k=top_k,
        )
