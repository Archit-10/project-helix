from app.rerankers.base import Reranker
from app.schemas.search_result import SearchResult


class ScoreBasedReranker(Reranker):
    """Reranks results using their existing relevance scores."""

    def rerank(
        self,
        query: str,
        results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )[:top_k]
