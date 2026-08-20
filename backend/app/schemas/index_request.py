from pydantic import BaseModel, Field


class IndexRequest(BaseModel):
    """Request for indexing a local document."""

    path: str = Field(min_length=1)
