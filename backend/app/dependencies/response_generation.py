from functools import lru_cache

from app.dependencies.llm import get_llm
from app.dependencies.retrieval import get_retrieval_service
from app.services.prompt_builder import PromptBuilder
from app.services.response_generation import ResponseGenerationService


@lru_cache
def get_response_generation_service() -> ResponseGenerationService:
    return ResponseGenerationService(
        retrieval_service=get_retrieval_service(),
        prompt_builder=PromptBuilder(),
        llm=get_llm(),
    )
