from app.embeddings.base import EmbeddingProvider
from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding


class EmbeddingService:
    """Coordinates embedding generation."""

    def __init__(
        self,
        provider: EmbeddingProvider,
    ) -> None:
        self.provider = provider

    def embed(
        self,
        chunk: DocumentChunk,
    ) -> Embedding:
        return self.provider.embed(chunk)

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return self.provider.embed_text(text)
