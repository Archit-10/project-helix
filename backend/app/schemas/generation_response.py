from pydantic import BaseModel

from app.schemas.citation import Citation


class GenerationResponse(BaseModel):
    answer: str
    citations: list[Citation]
