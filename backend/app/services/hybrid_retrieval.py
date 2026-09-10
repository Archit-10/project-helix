from app.core.cache import Cache
from app.rerankers.base import Reranker
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult
from app.services.lexical_retrieval import LexicalRetrievalService
from app.services.retrieval import SemanticRetrievalService


class HybridRetrievalService:
    """Combines semantic and lexical retrieval results."""

    CACHE_TTL_SECONDS = 300

    def __init__(
        self,
        semantic_service: SemanticRetrievalService,
        lexical_service: LexicalRetrievalService,
        reranker: Reranker,
        cache: Cache,
        semantic_weight: float = 0.5,
        lexical_weight: float = 0.5,
    ) -> None:
        if semantic_weight < 0 or lexical_weight < 0:
            raise ValueError("retrieval weights cannot be negative")

        self.semantic_service = semantic_service
        self.lexical_service = lexical_service
        self.reranker = reranker
        self.cache = cache
        self.semantic_weight = semantic_weight
        self.lexical_weight = lexical_weight

    def _build_cache_key(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None,
    ) -> str:
        """Builds a deterministic cache key for a retrieval request."""

        filter_key = None

        if metadata_filter is not None:
            filter_key = (
                metadata_filter.file_name,
                metadata_filter.extension,
                str(metadata_filter.path) if metadata_filter.path is not None else None,
                metadata_filter.content_hash,
            )

        return f"retrieval:{query}:{top_k}:{filter_key}"

    def search(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        cache_key = self._build_cache_key(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        cached_results = self.cache.get(cache_key)

        if cached_results is not None:
            return cached_results

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
        result_map: dict[tuple[str, str], SearchResult] = {}

        for result in semantic_results:
            key = (result.document_id, result.chunk_id)

            scores[key] = scores.get(key, 0.0) + (self.semantic_weight * result.score)

            result_map[key] = result

        for result in lexical_results:
            key = (result.document_id, result.chunk_id)

            scores[key] = scores.get(key, 0.0) + (self.lexical_weight * result.score)

            if key not in result_map:
                result_map[key] = result

        ranked_results = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        candidates = [
            SearchResult(
                document_id=document_id,
                chunk_id=chunk_id,
                score=score,
                content=result_map[(document_id, chunk_id)].content,
                metadata=result_map[(document_id, chunk_id)].metadata,
            )
            for (document_id, chunk_id), score in ranked_results
        ]

        results = self.reranker.rerank(
            query=query,
            results=candidates,
            top_k=top_k,
        )

        self.cache.set(
            cache_key,
            results,
            ttl_seconds=self.CACHE_TTL_SECONDS,
        )

        return results
