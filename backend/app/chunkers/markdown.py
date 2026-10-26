import re
from uuid import uuid4

from app.chunkers.base import Chunker
from app.schemas.document_chunk import DocumentChunk
from app.schemas.normalized_document import NormalizedDocument


class MarkdownChunker(Chunker):
    """Splits Markdown documents by headings and paragraph boundaries."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
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
        sections = re.split(
            r"(?m)(?=^#{1,6}\s+)",
            document.content,
        )

        chunks: list[DocumentChunk] = []

        for section in sections:
            section = section.strip()
            if not section:
                continue

            paragraphs = re.split(r"\n\s*\n", section)
            current = ""

            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    continue

                if len(paragraph) > self.chunk_size:
                    if current:
                        chunks.extend(self._make_chunks(document, current))
                        current = ""

                    chunks.extend(self._make_chunks(document, paragraph))
                    continue

                candidate = f"{current}\n\n{paragraph}" if current else paragraph

                if len(candidate) <= self.chunk_size:
                    current = candidate
                else:
                    if current:
                        chunks.extend(self._make_chunks(document, current))
                    current = paragraph

            if current:
                chunks.extend(self._make_chunks(document, current))

        return [
            chunk.model_copy(update={"chunk_index": index})
            for index, chunk in enumerate(chunks)
        ]

    def _make_chunks(
        self,
        document: NormalizedDocument,
        content: str,
    ) -> list[DocumentChunk]:
        chunks = []
        step = self.chunk_size - self.chunk_overlap

        for start in range(0, len(content), step):
            piece = content[start : start + self.chunk_size]
            if not piece:
                continue

            chunks.append(
                DocumentChunk(
                    document_id=document.metadata.content_hash,
                    chunk_id=str(uuid4()),
                    chunk_index=0,
                    content=piece,
                    metadata=document.metadata,
                )
            )

        return chunks
