from app.evaluation.dataset import EvaluationDataset
from app.services.evaluation import EvaluationService


class EvaluationRunner:
    """Runs evaluation cases through the evaluation service."""

    def __init__(self, evaluation_service: EvaluationService) -> None:
        self.evaluation_service = evaluation_service

    def run(
        self,
        dataset: EvaluationDataset,
        k: int,
    ) -> list[dict[str, dict[str, float]]]:
        """Evaluates all cases in a dataset."""
        return [
            self.evaluation_service.evaluate(
                case=case,
                k=k,
            )
            for case in dataset
        ]
