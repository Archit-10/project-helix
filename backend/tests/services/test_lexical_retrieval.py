from unittest.mock import Mock

from app.lexical_store.base import LexicalStore
from app.schemas.search_result import SearchResult
from app.services.lexical_retrieval import LexicalRetrievalService


def test_lexical_retrieval():
    result = SearchResult(
        chunk_id="chunk-1",
        document_id="doc-1",
        score=2.5,
    )

    lexical_store = Mock(spec=LexicalStore)
    lexical_store.search.return_value = [result]

    service = LexicalRetrievalService(
        lexical_store=lexical_store,
    )

    actual = service.search(
        query="Kafka authentication",
        top_k=5,
    )

    assert actual == [result]

    lexical_store.search.assert_called_once_with(
        query="Kafka authentication",
        top_k=5,
    )
