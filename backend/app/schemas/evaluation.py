from pydantic import BaseModel, Field

from app.schemas.search_result import SearchResult


class EvaluationCase(BaseModel):
    """Represents a single RAG evaluation case."""

    query: str
    expected_chunk_ids: list[str] = Field(default_factory=list)
    retrieved_results: list[SearchResult] = Field(default_factory=list)
    cited_chunk_ids: list[str] = Field(default_factory=list)
    generated_answer: str | None = None
    expected_answer: str | None = None
