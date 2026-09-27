from rank_bm25 import BM25Okapi

from app.lexical_store.base import LexicalStore
from app.schemas.document_chunk import DocumentChunk
from app.schemas.metadata_filter import MetadataFilter
from app.schemas.search_result import SearchResult
from app.utils.metadata_filter import matches_metadata


class BM25Store(LexicalStore):
    """BM25-based lexical search store."""

    def __init__(self) -> None:
        self.chunks: list[DocumentChunk] = []
        self.index: BM25Okapi | None = None

    def add(self, chunk: DocumentChunk) -> None:
        self.chunks.append(chunk)

        tokenized_corpus = [
            existing.content.lower().split() for existing in self.chunks
        ]

        self.index = BM25Okapi(tokenized_corpus)

    def search(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if not self.chunks:
            return []

        query_tokens = query.lower().split()

        scores = self.index.get_scores(query_tokens)

        ranked_indices = sorted(
            (
                index
                for index, chunk in enumerate(self.chunks)
                if set(query_tokens) & set(chunk.content.lower().split())
                and matches_metadata(
                    chunk.metadata,
                    metadata_filter,
                )
            ),
            key=lambda index: scores[index],
            reverse=True,
        )

        return [
            SearchResult(
                chunk_id=self.chunks[index].chunk_id,
                document_id=self.chunks[index].document_id,
                score=float(scores[index]),
                content=self.chunks[index].content,
                metadata=self.chunks[index].metadata,
            )
            for index in ranked_indices[:top_k]
        ]

    def delete(self, document_id: str) -> None:
        self.chunks = [
            chunk for chunk in self.chunks if chunk.document_id != document_id
        ]

        if self.chunks:
            tokenized_corpus = [chunk.content.lower().split() for chunk in self.chunks]

            self.index = BM25Okapi(tokenized_corpus)
        else:
            self.index = None
