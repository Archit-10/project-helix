from functools import lru_cache

from app.dependencies.cache import get_cache
from app.dependencies.stores import (
    get_lexical_store,
    get_vector_store,
)
from app.embeddings.sentence_transformer import SentenceTransformerProvider
from app.rerankers.score_based import ScoreBasedReranker
from app.services.embedding import EmbeddingService
from app.services.hybrid_retrieval import HybridRetrievalService
from app.services.lexical_retrieval import LexicalRetrievalService
from app.services.retrieval import SemanticRetrievalService


@lru_cache
def get_retrieval_service() -> HybridRetrievalService:
    embedding_provider = SentenceTransformerProvider()

    embedding_service = EmbeddingService(
        provider=embedding_provider,
    )

    vector_store = get_vector_store()
    lexical_store = get_lexical_store()

    semantic_service = SemanticRetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    lexical_service = LexicalRetrievalService(
        lexical_store=lexical_store,
    )

    reranker = ScoreBasedReranker()
    cache = get_cache()

    return HybridRetrievalService(
        semantic_service=semantic_service,
        lexical_service=lexical_service,
        reranker=reranker,
        cache=cache,
    )
