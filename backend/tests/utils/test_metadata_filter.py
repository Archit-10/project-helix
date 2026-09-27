from datetime import datetime
from pathlib import Path

from app.schemas.document_metadata import DocumentMetadata
from app.schemas.metadata_filter import MetadataFilter
from app.utils.metadata_filter import matches_metadata


def create_metadata() -> DocumentMetadata:
    return DocumentMetadata(
        file_name="security.md",
        extension=".md",
        path=Path("docs/security.md"),
        size_bytes=100,
        last_modified=datetime.now(),
        content_hash="hash-123",
    )


def test_matches_metadata_without_filter():
    metadata = create_metadata()

    assert matches_metadata(metadata, None)


def test_matches_metadata_by_file_name():
    metadata = create_metadata()

    metadata_filter = MetadataFilter(
        file_name="security.md",
    )

    assert matches_metadata(metadata, metadata_filter)


def test_rejects_metadata_with_wrong_file_name():
    metadata = create_metadata()

    metadata_filter = MetadataFilter(
        file_name="architecture.md",
    )

    assert not matches_metadata(metadata, metadata_filter)


def test_matches_multiple_fields():
    metadata = create_metadata()

    metadata_filter = MetadataFilter(
        file_name="security.md",
        extension=".md",
        content_hash="hash-123",
    )

    assert matches_metadata(metadata, metadata_filter)


def test_rejects_when_any_field_does_not_match():
    metadata = create_metadata()

    metadata_filter = MetadataFilter(
        file_name="security.md",
        extension=".pdf",
    )

    assert not matches_metadata(metadata, metadata_filter)
