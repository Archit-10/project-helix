from app.schemas.evaluation import EvaluationCase


def test_evaluation_case_defaults():
    case = EvaluationCase(
        query="How does authentication work?",
    )

    assert case.query == "How does authentication work?"
    assert case.expected_chunk_ids == []
    assert case.retrieved_results == []
    assert case.generated_answer is None
    assert case.expected_answer is None


def test_evaluation_case_accepts_expected_and_retrieved_chunks():
    case = EvaluationCase(
        query="How does authentication work?",
        expected_chunk_ids=["chunk-1", "chunk-2"],
    )

    assert case.expected_chunk_ids == [
        "chunk-1",
        "chunk-2",
    ]


def test_evaluation_case_accepts_answers():
    case = EvaluationCase(
        query="How does authentication work?",
        generated_answer="Authentication uses JWT tokens.",
        expected_answer="Authentication uses JWT-based access tokens.",
    )

    assert case.generated_answer == ("Authentication uses JWT tokens.")
    assert case.expected_answer == ("Authentication uses JWT-based access tokens.")
