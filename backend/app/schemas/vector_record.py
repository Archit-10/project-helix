from pydantic import BaseModel


class VectorRecord(BaseModel):
    """Represents a vector stored in the vector index."""

    chunk_id: str
    document_id: str
    vector: list[float]
