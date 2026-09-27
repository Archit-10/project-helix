from pydantic import BaseModel

from app.schemas.document_metadata import DocumentMetadata


class VectorRecord(BaseModel):
    """Represents a vector stored in the vector index."""

    chunk_id: str
    document_id: str
    vector: list[float]
    content: str
    metadata: DocumentMetadata
