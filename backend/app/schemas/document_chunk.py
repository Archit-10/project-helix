from pydantic import BaseModel

from app.schemas.document_metadata import DocumentMetadata


class DocumentChunk(BaseModel):
    """Represents a chunk produced from a normalized document."""

    document_id: str
    chunk_id: str
    chunk_index: int
    content: str
    metadata: DocumentMetadata
