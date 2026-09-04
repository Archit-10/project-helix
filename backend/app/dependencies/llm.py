from functools import lru_cache

from app.config.settings import get_settings
from app.llm.ollama import OllamaLLM


@lru_cache
def get_llm() -> OllamaLLM:
    return OllamaLLM(
        settings=get_settings(),
    )
