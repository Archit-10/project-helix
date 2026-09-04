from pydantic import BaseModel


class GenerationResponse(BaseModel):
    answer: str
