from app.evaluation.dataset import EvaluationDataset
from app.schemas.evaluation import EvaluationCase


def test_evaluation_dataset_stores_cases():
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

    assert len(dataset) == 2
    assert dataset.cases == cases


def test_evaluation_dataset_is_iterable():
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

    assert list(dataset) == cases
