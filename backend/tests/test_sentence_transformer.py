from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import numpy as np

from app.embeddings.sentence_transformer import SentenceTransformerProvider
from app.schemas.document_chunk import DocumentChunk
from app.schemas.document_metadata import DocumentMetadata


def test_sentence_transformer_provider():
    chunk = DocumentChunk(
        document_id="doc-1",
        chunk_id="chunk-1",
        chunk_index=0,
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

    fake_vector = np.array([0.1, 0.2, 0.3])

    with patch("app.embeddings.sentence_transformer.SentenceTransformer") as mock_model:
        mock_model.return_value.encode.return_value = fake_vector

        provider = SentenceTransformerProvider()

        result = provider.embed(chunk)

    assert result.chunk_id == "chunk-1"
    assert result.document_id == "doc-1"
    assert result.vector == [0.1, 0.2, 0.3]
