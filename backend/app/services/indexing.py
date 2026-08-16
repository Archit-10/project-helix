from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding
from app.schemas.normalized_document import NormalizedDocument
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService


class IndexingService:
    """Coordinates document chunking and embedding."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
    ) -> None:
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service

    def index(
        self,
        document: NormalizedDocument,
    ) -> tuple[list[DocumentChunk], list[Embedding]]:
        chunks = self.chunking_service.chunk(document)

        embeddings = [self.embedding_service.embed(chunk) for chunk in chunks]

        return chunks, embeddings
