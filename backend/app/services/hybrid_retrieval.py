from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult
from app.services.lexical_retrieval import LexicalRetrievalService
from app.services.retrieval import SemanticRetrievalService


class HybridRetrievalService:
    """Combines semantic and lexical retrieval results."""

    def __init__(
        self,
        semantic_service: SemanticRetrievalService,
        lexical_service: LexicalRetrievalService,
        semantic_weight: float = 0.5,
        lexical_weight: float = 0.5,
    ) -> None:
        if semantic_weight < 0 or lexical_weight < 0:
            raise ValueError("retrieval weights cannot be negative")

        self.semantic_service = semantic_service
        self.lexical_service = lexical_service
        self.semantic_weight = semantic_weight
        self.lexical_weight = lexical_weight

    def search(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        semantic_results = self.semantic_service.search(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        lexical_results = self.lexical_service.search(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        scores: dict[tuple[str, str], float] = {}

        for result in semantic_results:
            key = (result.document_id, result.chunk_id)
            scores[key] = scores.get(key, 0.0) + (self.semantic_weight * result.score)

        for result in lexical_results:
            key = (result.document_id, result.chunk_id)
            scores[key] = scores.get(key, 0.0) + (self.lexical_weight * result.score)

        ranked_results = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            SearchResult(
                document_id=document_id,
                chunk_id=chunk_id,
                score=score,
            )
            for (document_id, chunk_id), score in ranked_results[:top_k]
        ]
