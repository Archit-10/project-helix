from unittest.mock import Mock

from app.schemas.search_result import SearchResult
from app.services.embedding import EmbeddingService
from app.services.retrieval import SemanticRetrievalService
from app.vector_store.base import VectorStore


def test_semantic_retrieval(metadata):
    query = "How does authentication work?"

    results = [
        SearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            score=0.98,
            content="Authentication content.",
            metadata=metadata,
        )
    ]

    embedding_service = Mock(spec=EmbeddingService)
    vector_store = Mock(spec=VectorStore)

    embedding_service.embed_text.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    vector_store.search.return_value = results

    service = SemanticRetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    actual = service.search(
        query=query,
        top_k=5,
    )

    assert actual == results

    embedding_service.embed_text.assert_called_once_with(query)

    vector_store.search.assert_called_once_with(
        vector=[0.1, 0.2, 0.3],
        top_k=5,
        metadata_filter=None,
    )
