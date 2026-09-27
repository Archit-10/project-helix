from pathlib import Path

from pydantic import BaseModel


class MetadataFilter(BaseModel):
    """Filters retrieval results using document metadata."""

    file_name: str | None = None
    extension: str | None = None
    path: Path | None = None
    content_hash: str | None = None
