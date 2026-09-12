from unittest.mock import Mock

from app.evaluation.dataset import EvaluationDataset
from app.evaluation.runner import EvaluationRunner
from app.schemas.evaluation import EvaluationCase


def test_evaluation_runner_runs_all_cases():
    cases = [
        EvaluationCase(
            query="How does authentication work?",
            expected_chunk_ids=["chunk-1"],
        ),
        EvaluationCase(
            query="How does authorization work?",
            expected_chunk_ids=["chunk-2"],
        ),
    ]
    dataset = EvaluationDataset(cases=cases)

    evaluation_service = Mock()

    evaluation_service.evaluate.side_effect = [
        {
            "retrieval": {
                "recall_at_k": 1.0,
                "precision_at_k": 1.0,
                "mrr": 1.0,
            },
            "citations": {
                "citation_precision": 1.0,
            },
            "answer": {
                "exact_match": 1.0,
            },
        },
        {
            "retrieval": {
                "recall_at_k": 0.5,
                "precision_at_k": 0.5,
                "mrr": 0.5,
            },
            "citations": {
                "citation_precision": 0.5,
            },
            "answer": {
                "exact_match": 0.0,
            },
        },
    ]

    runner = EvaluationRunner(
        evaluation_service=evaluation_service,
    )

    results = runner.run(
        dataset=dataset,
        k=3,
    )

    assert len(results) == 2
    assert results[0]["retrieval"]["recall_at_k"] == 1.0
    assert results[1]["answer"]["exact_match"] == 0.0

    assert evaluation_service.evaluate.call_count == 2
