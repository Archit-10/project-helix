from app.lexical_store.base import LexicalStore
from app.schemas.search_result import SearchResult


class LexicalRetrievalService:
    """Retrieves relevant chunks using lexical search."""

    def __init__(
        self,
        lexical_store: LexicalStore,
    ) -> None:
        self.lexical_store = lexical_store

    def search(
        self,
        query: str,
        top_k: int,
    ) -> list[SearchResult]:
        return self.lexical_store.search(
            query=query,
            top_k=top_k,
        )
