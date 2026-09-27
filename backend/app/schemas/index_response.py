from pydantic import BaseModel


class IndexResponse(BaseModel):
    """Response returned after indexing a document."""

    document_id: str
    chunks_indexed: int
