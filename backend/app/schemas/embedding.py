from pydantic import BaseModel


class Embedding(BaseModel):
    """Represents the embedding generated for a document chunk."""

    chunk_id: str
    document_id: str
    vector: list[float]
