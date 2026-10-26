from app.chunkers.base import Chunker
from app.chunkers.fixed_size import FixedSizeChunker
from app.chunkers.markdown import MarkdownChunker
from app.schemas.document_chunk import DocumentChunk
from app.schemas.normalized_document import NormalizedDocument


class ChunkingService:
    """Selects a chunking strategy based on document format."""

    def __init__(
        self,
        chunker: Chunker | None = None,
        markdown_chunker: Chunker | None = None,
    ) -> None:
        self.chunker = chunker or FixedSizeChunker()
        self.markdown_chunker = markdown_chunker or MarkdownChunker()

    def chunk(
        self,
        document: NormalizedDocument,
    ) -> list[DocumentChunk]:
        extension = document.metadata.extension.lower()

        if extension in {".md", ".markdown"}:
            return self.markdown_chunker.chunk(document)

        return self.chunker.chunk(document)
