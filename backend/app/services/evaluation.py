from app.evaluation.answer import AnswerEvaluator
from app.evaluation.citations import CitationEvaluator
from app.evaluation.retrieval import RetrievalEvaluator
from app.schemas.evaluation import EvaluationCase


class EvaluationService:
    """Runs evaluation metrics for RAG evaluation cases."""

    def __init__(
        self,
        retrieval_evaluator: RetrievalEvaluator,
        citation_evaluator: CitationEvaluator,
        answer_evaluator: AnswerEvaluator,
    ) -> None:
        self.retrieval_evaluator = retrieval_evaluator
        self.citation_evaluator = citation_evaluator
        self.answer_evaluator = answer_evaluator

    def evaluate_retrieval(
        self,
        case: EvaluationCase,
        k: int,
    ) -> dict[str, float]:
        """Evaluates retrieval quality for an evaluation case."""

        retrieved_chunk_ids = [result.chunk_id for result in case.retrieved_results]

        return {
            "recall_at_k": self.retrieval_evaluator.recall_at_k(
                expected_chunk_ids=case.expected_chunk_ids,
                retrieved_chunk_ids=retrieved_chunk_ids,
                k=k,
            ),
            "precision_at_k": self.retrieval_evaluator.precision_at_k(
                expected_chunk_ids=case.expected_chunk_ids,
                retrieved_chunk_ids=retrieved_chunk_ids,
                k=k,
            ),
            "mrr": self.retrieval_evaluator.mean_reciprocal_rank(
                expected_chunk_ids=case.expected_chunk_ids,
                retrieved_chunk_ids=retrieved_chunk_ids,
            ),
        }

    def evaluate_citations(
        self,
        case: EvaluationCase,
    ) -> dict[str, float]:
        """Evaluates citation quality for an evaluation case."""

        return {
            "citation_precision": (
                self.citation_evaluator.citation_precision(
                    expected_chunk_ids=case.expected_chunk_ids,
                    cited_chunk_ids=case.cited_chunk_ids,
                )
            ),
        }

    def evaluate_answer(
        self,
        case: EvaluationCase,
    ) -> dict[str, float]:
        """Evaluates generated answer quality."""

        if case.generated_answer is None or case.expected_answer is None:
            return {
                "exact_match": 0.0,
            }

        return {
            "exact_match": self.answer_evaluator.exact_match(
                expected_answer=case.expected_answer,
                generated_answer=case.generated_answer,
            ),
        }

    def evaluate(
        self,
        case: EvaluationCase,
        k: int,
    ) -> dict[str, dict[str, float]]:
        """Evaluates retrieval, citations, and answer quality."""

        return {
            "retrieval": self.evaluate_retrieval(
                case=case,
                k=k,
            ),
            "citations": self.evaluate_citations(
                case=case,
            ),
            "answer": self.evaluate_answer(
                case=case,
            ),
        }
