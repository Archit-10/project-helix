from pathlib import Path

from app.providers.markdown import MarkdownProvider
from app.services.ingestion import IngestionService


def test_markdown_ingestion():
    service = IngestionService(
        providers=[
            MarkdownProvider(),
        ]
    )

    document = service.ingest(Path("sample_documents/hello.md"))

    # Metadata assertions
    assert document.metadata.file_name == "hello.md"
    assert document.metadata.extension == ".md"
    assert document.metadata.size_bytes > 0
    assert document.metadata.content_hash != ""

    # Content assertions
    assert document.content.startswith("# Project Helix")
    assert "ingestion pipeline" in document.content
