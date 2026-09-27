from datetime import datetime
from hashlib import sha256
from pathlib import Path

from app.schemas.document_metadata import DocumentMetadata


def build_document_metadata(path: Path, content: str) -> DocumentMetadata:
    stat = path.stat()

    return DocumentMetadata(
        file_name=path.name,
        extension=path.suffix.lower(),
        path=path.resolve(),
        size_bytes=stat.st_size,
        last_modified=datetime.fromtimestamp(stat.st_mtime),
        content_hash=sha256(content.encode("utf-8")).hexdigest(),
    )
