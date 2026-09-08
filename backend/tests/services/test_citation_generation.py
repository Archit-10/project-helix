from app.schemas.citation import Citation
from app.schemas.search_result import SearchResult
from app.services.citation_generation import CitationGenerator


def test_citation_generation(metadata):
    results = [
        SearchResult(
            document_id="doc-1",
            chunk_id="chunk-1",
            score=0.95,
            content="Kafka authentication content.",
            metadata=metadata,
        )
    ]

    generator = CitationGenerator()

    citations = generator.generate(results)

    assert citations == [
        Citation(
            document_id="doc-1",
            chunk_id="chunk-1",
            file_name=metadata.file_name,
            path=metadata.path,
        )
    ]


def test_citation_generation_multiple_results(metadata):
    results = [
        SearchResult(
            document_id="doc-1",
            chunk_id="chunk-1",
            score=0.95,
            content="Kafka authentication content.",
            metadata=metadata,
        ),
        SearchResult(
            document_id="doc-2",
            chunk_id="chunk-2",
            score=0.87,
            content="TLS encryption content.",
            metadata=metadata,
        ),
    ]

    generator = CitationGenerator()

    citations = generator.generate(results)

    assert len(citations) == 2

    assert citations[0].document_id == "doc-1"
    assert citations[0].chunk_id == "chunk-1"

    assert citations[1].document_id == "doc-2"
    assert citations[1].chunk_id == "chunk-2"


def test_citation_generation_empty_results():
    generator = CitationGenerator()

    citations = generator.generate([])

    assert citations == []
