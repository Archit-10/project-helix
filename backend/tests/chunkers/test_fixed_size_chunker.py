from datetime import datetime
from pathlib import Path

from app.chunkers.fixed_size import FixedSizeChunker
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.normalized_document import NormalizedDocument


def test_fixed_size_chunker():
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

    chunker = FixedSizeChunker(
        chunk_size=10,
        chunk_overlap=2,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 4
    assert chunks[0].content == "abcdefghij"
    assert chunks[1].content == "ijklmnopqr"
    assert chunks[2].content == "qrstuvwxyz"
