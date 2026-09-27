from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    file_name: str
    extension: str

    path: Path

    size_bytes: int

    last_modified: datetime

    content_hash: str
