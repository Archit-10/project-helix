from app.lexical_store.base import LexicalStore
from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding
from app.schemas.normalized_document import NormalizedDocument
from app.schemas.vector_record import VectorRecord
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.vector_store.base import VectorStore


class IndexingService:
    """Coordinates document chunking, embedding, and indexing."""

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        lexical_store: LexicalStore,
        vector_store: VectorStore,
    ) -> None:
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.lexical_store = lexical_store
        self.vector_store = vector_store

    def index(
        self,
        document: NormalizedDocument,
    ) -> tuple[list[DocumentChunk], list[Embedding]]:
        document_id = document.metadata.content_hash

        self.lexical_store.delete(document_id)
        self.vector_store.delete(document_id)

        chunks = self.chunking_service.chunk(document)

        embeddings = []

        for chunk in chunks:
            embedding = self.embedding_service.embed(chunk)

            self.lexical_store.add(chunk)

            self.vector_store.add(
                VectorRecord(
                    chunk_id=embedding.chunk_id,
                    document_id=embedding.document_id,
                    vector=embedding.vector,
                    metadata=chunk.metadata,
                    content=chunk.content,
                )
            )

            embeddings.append(embedding)

        return chunks, embeddings
