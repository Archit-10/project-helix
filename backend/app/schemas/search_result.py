from pydantic import BaseModel


class SearchResult(BaseModel):
    """Represents a retrieved result with a relevance score."""

    chunk_id: str
    document_id: str
    score: float
    content: str
