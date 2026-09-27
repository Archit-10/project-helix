from pathlib import Path

from pydantic import BaseModel


class Citation(BaseModel):
    document_id: str
    chunk_id: str
    file_name: str
    path: Path
