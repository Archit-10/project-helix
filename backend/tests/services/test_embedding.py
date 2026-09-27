from unittest.mock import MagicMock

from app.schemas.document_chunk import DocumentChunk
from app.schemas.embedding import Embedding
from app.services.embedding import EmbeddingService


def test_embedding_service():
    chunk = MagicMock(spec=DocumentChunk)

    expected = Embedding(
        chunk_id="chunk-1",
        document_id="doc-1",
        vector=[0.1, 0.2, 0.3],
    )

    provider = MagicMock()
    provider.embed.return_value = expected

    service = EmbeddingService(provider=provider)

    result = service.embed(chunk)

    assert result == expected
    provider.embed.assert_called_once_with(chunk)


def test_embedding_service_text():
    provider = MagicMock()

    expected = [0.1, 0.2, 0.3]

    provider.embed_text.return_value = expected

    service = EmbeddingService(provider=provider)

    result = service.embed_text("How does authentication work?")

    assert result == expected
    provider.embed_text.assert_called_once_with("How does authentication work?")
