from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

from app.schemas.document_chunk import DocumentChunk
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.embedding import Embedding
from app.schemas.normalized_document import NormalizedDocument
from app.schemas.vector_record import VectorRecord
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.indexing import IndexingService


def test_indexing_service():
    document = NormalizedDocument(
        content="Project Helix is a RAG platform.",
        metadata=DocumentMetadata(
            file_name="sample.txt",
            extension=".txt",
            path=Path("sample_documents/sample.txt"),
            size_bytes=100,
            last_modified=datetime.now(),
            content_hash="dummy-hash",
        ),
    )

    chunk = DocumentChunk(
        document_id="doc-1",
        chunk_id="chunk-1",
        chunk_index=0,
        content="Project Helix is a RAG platform.",
        metadata=document.metadata,
    )

    embedding = Embedding(
        chunk_id="chunk-1",
        document_id="doc-1",
        vector=[0.1, 0.2, 0.3],
    )

    chunking_service = Mock(spec=ChunkingService)
    embedding_service = Mock(spec=EmbeddingService)

    lexical_store = Mock()
    vector_store = Mock()

    chunking_service.chunk.return_value = [chunk]
    embedding_service.embed.return_value = embedding

    service = IndexingService(
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        lexical_store=lexical_store,
        vector_store=vector_store,
    )

    chunks, embeddings = service.index(document)

    assert chunks == [chunk]
    assert embeddings == [embedding]

    chunking_service.chunk.assert_called_once_with(document)
    embedding_service.embed.assert_called_once_with(chunk)

    lexical_store.add.assert_called_once_with(chunk)

    vector_store.add.assert_called_once_with(
        VectorRecord(
            chunk_id="chunk-1",
            document_id="doc-1",
            vector=[0.1, 0.2, 0.3],
        )
    )
