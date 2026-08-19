from functools import lru_cache

from app.lexical_store.bm25_store import BM25Store
from app.vector_store.faiss_store import FAISSVectorStore


@lru_cache
def get_vector_store() -> FAISSVectorStore:
    return FAISSVectorStore(dimension=384)


@lru_cache
def get_lexical_store() -> BM25Store:
    return BM25Store()
