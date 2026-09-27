from pydantic import BaseModel, Field

from app.schemas.metadata_filter import MetadataFilter


class SearchRequest(BaseModel):
    """Request for searching indexed documents."""

    query: str = Field(min_length=1)
    top_k: int = Field(default=5, gt=0)
    metadata_filter: MetadataFilter | None = None
