class RetrievalEvaluator:
    """Calculates retrieval evaluation metrics."""

    @staticmethod
    def recall_at_k(
        expected_chunk_ids: list[str],
        retrieved_chunk_ids: list[str],
        k: int,
    ) -> float:
        """Calculates Recall@K for retrieved chunks."""

        if k <= 0:
            raise ValueError("k must be greater than 0")

        if not expected_chunk_ids:
            return 0.0

        expected = set(expected_chunk_ids)
        retrieved = set(retrieved_chunk_ids[:k])

        return len(expected & retrieved) / len(expected)

    @staticmethod
    def precision_at_k(
        expected_chunk_ids: list[str],
        retrieved_chunk_ids: list[str],
        k: int,
    ) -> float:
        """Calculates Precision@K for retrieved chunks."""

        if k <= 0:
            raise ValueError("k must be greater than 0")

        if not retrieved_chunk_ids[:k]:
            return 0.0

        expected = set(expected_chunk_ids)
        retrieved = set(retrieved_chunk_ids[:k])

        return len(expected & retrieved) / len(retrieved)

    @staticmethod
    def mean_reciprocal_rank(
        expected_chunk_ids: list[str],
        retrieved_chunk_ids: list[str],
    ) -> float:
        """Calculates Mean Reciprocal Rank for a single query."""

        if not expected_chunk_ids:
            return 0.0

        expected = set(expected_chunk_ids)

        for rank, chunk_id in enumerate(
            retrieved_chunk_ids,
            start=1,
        ):
            if chunk_id in expected:
                return 1.0 / rank

        return 0.0
