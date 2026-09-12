class AnswerEvaluator:
    """Calculates answer evaluation metrics."""

    @staticmethod
    def exact_match(
        expected_answer: str,
        generated_answer: str,
    ) -> float:
        """Calculates normalized exact-match accuracy."""

        expected = " ".join(expected_answer.lower().split())
        generated = " ".join(generated_answer.lower().split())

        return 1.0 if expected == generated else 0.0
