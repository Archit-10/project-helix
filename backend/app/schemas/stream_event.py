from typing import Literal

from pydantic import BaseModel

from app.schemas.citation import Citation


class StreamEvent(BaseModel):
    type: Literal["token", "citations", "done"]
    content: str | None = None
    citations: list[Citation] | None = None
