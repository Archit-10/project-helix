from pathlib import Path

from app.providers.text import TextProvider
from app.services.ingestion import IngestionService


def test_text_ingestion():
    service = IngestionService(
        providers=[
            TextProvider(),
        ]
    )

    document = service.ingest(Path("sample_documents/notes.txt"))

    assert document.metadata.file_name == "notes.txt"
    assert document.metadata.extension == ".txt"
    assert document.metadata.size_bytes > 0
    assert len(document.metadata.content_hash) == 64

    assert "provider-based ingestion" in document.content
