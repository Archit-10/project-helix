from app.chunkers.base import Chunker
from app.schemas.document_chunk import DocumentChunk
from app.schemas.normalized_document import NormalizedDocument


class ChunkingService:
    """Coordinates document chunking using a configured strategy."""

    def __init__(self, chunker: Chunker):
        self.chunker = chunker

    def chunk(
        self,
        document: NormalizedDocument,
    ) -> list[DocumentChunk]:
        return self.chunker.chunk(document)
