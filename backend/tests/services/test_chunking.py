from datetime import datetime
from pathlib import Path

from app.chunkers.fixed_size import FixedSizeChunker
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.normalized_document import NormalizedDocument
from app.services.chunking import ChunkingService


def test_chunking_service():
    document = NormalizedDocument(
        content="abcdefghijklmnopqrstuvwxyz",
        metadata=DocumentMetadata(
            file_name="sample.txt",
            extension=".txt",
            path=Path("sample_documents/sample.txt"),
            size_bytes=26,
            last_modified=datetime.now(),
            content_hash="dummy-hash",
        ),
    )

    service = ChunkingService(
        chunker=FixedSizeChunker(
            chunk_size=10,
            chunk_overlap=2,
        )
    )

    chunks = service.chunk(document)

    assert len(chunks) == 4

    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1

    assert chunks[0].metadata.file_name == "sample.txt"

    assert all(chunk.document_id == "dummy-hash" for chunk in chunks)
