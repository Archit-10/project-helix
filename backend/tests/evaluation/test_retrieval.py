import pytest

from app.evaluation.retrieval import RetrievalEvaluator


def test_recall_at_k():
    score = RetrievalEvaluator.recall_at_k(
        expected_chunk_ids=["chunk-1", "chunk-2", "chunk-3"],
        retrieved_chunk_ids=[
            "chunk-1",
            "chunk-4",
            "chunk-2",
            "chunk-5",
        ],
        k=3,
    )

    assert score == pytest.approx(2 / 3)


def test_recall_at_k_all_expected_chunks_retrieved():
    score = RetrievalEvaluator.recall_at_k(
        expected_chunk_ids=["chunk-1", "chunk-2"],
        retrieved_chunk_ids=["chunk-2", "chunk-1"],
        k=5,
    )

    assert score == 1.0


def test_recall_at_k_no_expected_chunks():
    score = RetrievalEvaluator.recall_at_k(
        expected_chunk_ids=[],
        retrieved_chunk_ids=["chunk-1"],
        k=5,
    )

    assert score == 0.0


def test_recall_at_k_invalid_k():
    with pytest.raises(
        ValueError,
        match="k must be greater than 0",
    ):
        RetrievalEvaluator.recall_at_k(
            expected_chunk_ids=["chunk-1"],
            retrieved_chunk_ids=["chunk-1"],
            k=0,
        )


def test_precision_at_k():
    score = RetrievalEvaluator.precision_at_k(
        expected_chunk_ids=["chunk-1", "chunk-2", "chunk-3"],
        retrieved_chunk_ids=[
            "chunk-1",
            "chunk-4",
            "chunk-2",
            "chunk-5",
        ],
        k=3,
    )

    assert score == pytest.approx(2 / 3)


def test_precision_at_k_all_results_relevant():
    score = RetrievalEvaluator.precision_at_k(
        expected_chunk_ids=["chunk-1", "chunk-2"],
        retrieved_chunk_ids=["chunk-1", "chunk-2"],
        k=5,
    )

    assert score == 1.0


def test_precision_at_k_no_relevant_results():
    score = RetrievalEvaluator.precision_at_k(
        expected_chunk_ids=["chunk-1"],
        retrieved_chunk_ids=["chunk-2", "chunk-3"],
        k=2,
    )

    assert score == 0.0


def test_precision_at_k_no_retrieved_results():
    score = RetrievalEvaluator.precision_at_k(
        expected_chunk_ids=["chunk-1"],
        retrieved_chunk_ids=[],
        k=5,
    )

    assert score == 0.0


def test_precision_at_k_invalid_k():
    with pytest.raises(
        ValueError,
        match="k must be greater than 0",
    ):
        RetrievalEvaluator.precision_at_k(
            expected_chunk_ids=["chunk-1"],
            retrieved_chunk_ids=["chunk-1"],
            k=0,
        )


def test_mean_reciprocal_rank_first_result_relevant():
    score = RetrievalEvaluator.mean_reciprocal_rank(
        expected_chunk_ids=["chunk-1", "chunk-2"],
        retrieved_chunk_ids=[
            "chunk-1",
            "chunk-3",
            "chunk-4",
        ],
    )

    assert score == 1.0


def test_mean_reciprocal_rank_second_result_relevant():
    score = RetrievalEvaluator.mean_reciprocal_rank(
        expected_chunk_ids=["chunk-1", "chunk-2"],
        retrieved_chunk_ids=[
            "chunk-3",
            "chunk-2",
            "chunk-4",
        ],
    )

    assert score == 0.5


def test_mean_reciprocal_rank_no_relevant_result():
    score = RetrievalEvaluator.mean_reciprocal_rank(
        expected_chunk_ids=["chunk-1"],
        retrieved_chunk_ids=[
            "chunk-2",
            "chunk-3",
        ],
    )

    assert score == 0.0


def test_mean_reciprocal_rank_no_expected_chunks():
    score = RetrievalEvaluator.mean_reciprocal_rank(
        expected_chunk_ids=[],
        retrieved_chunk_ids=["chunk-1"],
    )

    assert score == 0.0
