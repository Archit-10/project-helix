from pydantic import BaseModel


class Prompt(BaseModel):
    system_prompt: str
    user_prompt: str
