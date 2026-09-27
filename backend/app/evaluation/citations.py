class CitationEvaluator:
    """Calculates citation evaluation metrics."""

    @staticmethod
    def citation_precision(
        expected_chunk_ids: list[str],
        cited_chunk_ids: list[str],
    ) -> float:
        """Calculates the precision of cited chunks."""

        if not cited_chunk_ids:
            return 0.0

        expected = set(expected_chunk_ids)
        cited = set(cited_chunk_ids)

        return len(expected & cited) / len(cited)
