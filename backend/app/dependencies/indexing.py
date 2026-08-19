from functools import lru_cache

from app.chunkers.fixed_size import FixedSizeChunker
from app.dependencies.stores import (
    get_lexical_store,
    get_vector_store,
)
from app.embeddings.sentence_transformer import SentenceTransformerProvider
from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.services.indexing import IndexingService


@lru_cache
def get_indexing_service() -> IndexingService:
    chunker = FixedSizeChunker()

    chunking_service = ChunkingService(
        chunker=chunker,
    )

    embedding_provider = SentenceTransformerProvider()

    embedding_service = EmbeddingService(
        provider=embedding_provider,
    )

    return IndexingService(
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        lexical_store=get_lexical_store(),
        vector_store=get_vector_store(),
    )
