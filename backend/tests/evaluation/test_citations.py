import pytest

from app.evaluation.citations import CitationEvaluator


def test_citation_precision():
    score = CitationEvaluator.citation_precision(
        expected_chunk_ids=[
            "chunk-1",
            "chunk-2",
        ],
        cited_chunk_ids=[
            "chunk-1",
            "chunk-3",
        ],
    )

    assert score == pytest.approx(0.5)


def test_citation_precision_all_citations_relevant():
    score = CitationEvaluator.citation_precision(
        expected_chunk_ids=[
            "chunk-1",
            "chunk-2",
        ],
        cited_chunk_ids=[
            "chunk-1",
            "chunk-2",
        ],
    )

    assert score == 1.0


def test_citation_precision_no_relevant_citations():
    score = CitationEvaluator.citation_precision(
        expected_chunk_ids=["chunk-1"],
        cited_chunk_ids=[
            "chunk-2",
            "chunk-3",
        ],
    )

    assert score == 0.0


def test_citation_precision_no_citations():
    score = CitationEvaluator.citation_precision(
        expected_chunk_ids=["chunk-1"],
        cited_chunk_ids=[],
    )

    assert score == 0.0
