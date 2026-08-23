from abc import ABC, abstractmethod

from app.schemas.search_result import SearchResult


class Reranker(ABC):
    """Base interface for reranking retrieved search results."""

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:
        """Rerank retrieved results for the given query."""
