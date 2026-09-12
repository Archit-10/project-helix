from app.evaluation.answer import AnswerEvaluator


def test_exact_match():
    score = AnswerEvaluator.exact_match(
        expected_answer="JWT authentication is used.",
        generated_answer="JWT authentication is used.",
    )

    assert score == 1.0


def test_exact_match_ignores_case_and_whitespace():
    score = AnswerEvaluator.exact_match(
        expected_answer="JWT authentication is used.",
        generated_answer="  jwt   authentication IS used.  ",
    )

    assert score == 1.0


def test_exact_match_returns_zero_for_different_answers():
    score = AnswerEvaluator.exact_match(
        expected_answer="JWT authentication is used.",
        generated_answer="OAuth authentication is used.",
    )

    assert score == 0.0
