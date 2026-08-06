from uuid import uuid4

from app.chunkers.base import Chunker
from app.schemas.document_chunk import DocumentChunk
from app.schemas.normalized_document import NormalizedDocument


class FixedSizeChunker(Chunker):
    """Splits documents into fixed-size character chunks with overlap."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(
        self,
        document: NormalizedDocument,
    ) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        step = self.chunk_size - self.chunk_overlap

        for index, start in enumerate(range(0, len(document.content), step)):
            content = document.content[start : start + self.chunk_size]

            if not content:
                continue

            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    chunk_index=index,
                    content=content,
                    metadata=document.metadata,
                )
            )

        return chunks
