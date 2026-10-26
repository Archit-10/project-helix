from datetime import datetime
from pathlib import Path

from app.chunkers.markdown import MarkdownChunker
from app.schemas.document_metadata import DocumentMetadata
from app.schemas.normalized_document import NormalizedDocument


def make_document(content: str) -> NormalizedDocument:
    return NormalizedDocument(
        content=content,
        metadata=DocumentMetadata(
            file_name="incident-response.md",
            extension=".md",
            path=Path("demo-knowledge/incident-response.md"),
            size_bytes=len(content.encode("utf-8")),
            last_modified=datetime.now(),
            content_hash="test-hash",
        ),
    )


def test_markdown_chunker_preserves_heading_with_section():
    document = make_document(
        "# Incident Response\n\n"
        "Identify the incident and record its severity.\n\n"
        "## Containment\n\n"
        "Isolate affected workloads and revoke compromised credentials."
    )

    chunks = MarkdownChunker(chunk_size=1000).chunk(document)

    assert len(chunks) == 2
    assert chunks[0].content.startswith("# Incident Response")
    assert "Identify the incident" in chunks[0].content
    assert chunks[1].content.startswith("## Containment")
    assert "revoke compromised credentials" in chunks[1].content


def test_markdown_chunker_assigns_sequential_indices():
    document = make_document("# First\n\n" + "A" * 80 + "\n\n# Second\n\n" + "B" * 80)

    chunks = MarkdownChunker(
        chunk_size=100,
        chunk_overlap=20,
    ).chunk(document)

    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))


def test_markdown_chunker_preserves_document_metadata():
    document = make_document("# Incident\n\nInvestigate the alert.")

    chunks = MarkdownChunker().chunk(document)

    assert all(chunk.document_id == "test-hash" for chunk in chunks)
    assert all(chunk.metadata.file_name == "incident-response.md" for chunk in chunks)
