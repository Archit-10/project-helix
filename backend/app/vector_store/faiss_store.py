import faiss
import numpy as np

from app.schemas.search_result import SearchResult
from app.schemas.vector_record import VectorRecord
from app.vector_store.base import VectorStore


class FAISSVectorStore(VectorStore):
    """FAISS-backed vector store using cosine similarity."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        vector = np.array(
            [record.vector],
            dtype=np.float32,
        )

        faiss.normalize_L2(vector)

        self.index.add(vector)
        self.records.append(record)

    def search(
        self,
        vector: list[float],
        top_k: int,
    ) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if self.index.ntotal == 0:
            return []

        query = np.array(
            [vector],
            dtype=np.float32,
        )

        faiss.normalize_L2(query)

        scores, indices = self.index.search(
            query,
            min(top_k, self.index.ntotal),
        )

        return [
            SearchResult(
                chunk_id=self.records[index].chunk_id,
                document_id=self.records[index].document_id,
                score=float(scores[0][position]),
            )
            for position, index in enumerate(indices[0])
            if index != -1
        ]

    def delete(self, document_id: str) -> None:
        records_to_keep = [
            record for record in self.records if record.document_id != document_id
        ]

        self.index = faiss.IndexFlatIP(self.dimension)

        self.records = []

        for record in records_to_keep:
            self.add(record)
