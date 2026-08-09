from sentence_transformers import SentenceTransformer

from app.embeddings.base import EmbeddingProvider
from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding


class SentenceTransformerProvider(EmbeddingProvider):
    """Generates embeddings using a Sentence Transformer model."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, chunk: DocumentChunk) -> Embedding:
        vector = self.model.encode(
            chunk.content,
            convert_to_numpy=True,
        )

        return Embedding(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            vector=vector.tolist(),
        )
