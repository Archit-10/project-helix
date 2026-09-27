from collections.abc import Iterator

from app.schemas.evaluation import EvaluationCase


class EvaluationDataset:
    """Stores a collection of evaluation cases."""

    def __init__(self, cases: list[EvaluationCase]) -> None:
        self.cases = cases

    def __len__(self) -> int:
        return len(self.cases)

    def __iter__(self) -> Iterator[EvaluationCase]:
        """Iterates over evaluation cases."""
        return iter(self.cases)
