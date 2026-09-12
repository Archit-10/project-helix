from datetime import datetime
from pathlib import Path

from app.evaluation.answer import AnswerEvaluator
from app.evaluation.citations import CitationEvaluator
from app.evaluation.retrieval import RetrievalEvaluator
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.evaluation import EvaluationCase
from app.schemas.search_result import SearchResult
from app.services.evaluation import EvaluationService


def test_evaluate_retrieval():
    metadata = DocumentMetadata(
        file_name="auth.md",
        extension=".md",
        path=Path("docs/auth.md"),
        size_bytes=100,
        last_modified=datetime.now(),
        content_hash="hash-1",
    )

    case = EvaluationCase(
        query="How does authentication work?",
        expected_chunk_ids=[
            "chunk-1",
            "chunk-2",
            "chunk-3",
        ],
        retrieved_results=[
            SearchResult(
                chunk_id="chunk-1",
                document_id="doc-1",
                score=0.95,
                content="Authentication content.",
                metadata=metadata,
            ),
            SearchResult(
                chunk_id="chunk-4",
                document_id="doc-1",
                score=0.80,
                content="Unrelated content.",
                metadata=metadata,
            ),
            SearchResult(
                chunk_id="chunk-2",
                document_id="doc-1",
                score=0.75,
                content="JWT content.",
                metadata=metadata,
            ),
        ],
    )

    service = EvaluationService(
        retrieval_evaluator=RetrievalEvaluator(),
        citation_evaluator=CitationEvaluator(),
        answer_evaluator=AnswerEvaluator(),
    )

    metrics = service.evaluate_retrieval(
        case=case,
        k=3,
    )

    assert metrics["recall_at_k"] == 2 / 3
    assert metrics["precision_at_k"] == 2 / 3
    assert metrics["mrr"] == 1.0


def test_evaluate_citations():
    case = EvaluationCase(
        query="How does authentication work?",
        expected_chunk_ids=[
            "chunk-1",
            "chunk-2",
        ],
        cited_chunk_ids=[
            "chunk-1",
            "chunk-3",
        ],
    )

    service = EvaluationService(
        retrieval_evaluator=RetrievalEvaluator(),
        citation_evaluator=CitationEvaluator(),
        answer_evaluator=AnswerEvaluator(),
    )

    metrics = service.evaluate_citations(case)

    assert metrics["citation_precision"] == 0.5


def test_evaluate_answer():
    case = EvaluationCase(
        query="How does authentication work?",
        expected_answer="JWT authentication is used.",
        generated_answer="  jwt   authentication IS used.  ",
    )

    service = EvaluationService(
        retrieval_evaluator=RetrievalEvaluator(),
        citation_evaluator=CitationEvaluator(),
        answer_evaluator=AnswerEvaluator(),
    )

    metrics = service.evaluate_answer(case)

    assert metrics["exact_match"] == 1.0


def test_evaluate_answer_without_answers():
    case = EvaluationCase(
        query="How does authentication work?",
    )

    service = EvaluationService(
        retrieval_evaluator=RetrievalEvaluator(),
        citation_evaluator=CitationEvaluator(),
        answer_evaluator=AnswerEvaluator(),
    )

    metrics = service.evaluate_answer(case)

    assert metrics["exact_match"] == 0.0


def test_evaluate():
    metadata = DocumentMetadata(
        file_name="auth.md",
        extension=".md",
        path=Path("docs/auth.md"),
        size_bytes=100,
        last_modified=datetime.now(),
        content_hash="hash-1",
    )

    case = EvaluationCase(
        query="How does authentication work?",
        expected_chunk_ids=[
            "chunk-1",
            "chunk-2",
        ],
        retrieved_results=[
            SearchResult(
                chunk_id="chunk-1",
                document_id="doc-1",
                score=0.95,
                content="Authentication content.",
                metadata=metadata,
            ),
            SearchResult(
                chunk_id="chunk-3",
                document_id="doc-1",
                score=0.80,
                content="Unrelated content.",
                metadata=metadata,
            ),
        ],
        cited_chunk_ids=[
            "chunk-1",
            "chunk-3",
        ],
        expected_answer="JWT authentication is used.",
        generated_answer="jwt authentication IS used.",
    )

    service = EvaluationService(
        retrieval_evaluator=RetrievalEvaluator(),
        citation_evaluator=CitationEvaluator(),
        answer_evaluator=AnswerEvaluator(),
    )

    metrics = service.evaluate(
        case=case,
        k=2,
    )

    assert metrics["retrieval"]["recall_at_k"] == 1 / 2
    assert metrics["retrieval"]["precision_at_k"] == 1 / 2
    assert metrics["retrieval"]["mrr"] == 1.0

    assert metrics["citations"]["citation_precision"] == 1 / 2

    assert metrics["answer"]["exact_match"] == 1.0
