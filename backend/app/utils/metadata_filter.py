from app.schemas.document_metadata import DocumentMetadata
from app.schemas.metadata_filter import MetadataFilter


def matches_metadata(
    metadata: DocumentMetadata,
    metadata_filter: MetadataFilter | None,
) -> bool:
    """Return whether metadata satisfies the provided filter."""

    if metadata_filter is None:
        return True

    if (
        metadata_filter.file_name is not None
        and metadata.file_name != metadata_filter.file_name
    ):
        return False

    if (
        metadata_filter.extension is not None
        and metadata.extension != metadata_filter.extension
    ):
        return False

    if metadata_filter.path is not None and metadata.path != metadata_filter.path:
        return False

    if (
        metadata_filter.content_hash is not None
        and metadata.content_hash != metadata_filter.content_hash
    ):
        return False

    return True
