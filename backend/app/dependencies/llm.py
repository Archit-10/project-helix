from functools import lru_cache

from app.config.settings import get_settings
from app.llm.base import LLM
from app.llm.groq import GroqLLM
from app.llm.ollama import OllamaLLM


@lru_cache
def get_llm() -> LLM:
    settings = get_settings()

    if settings.LLM_PROVIDER == "ollama":
        return OllamaLLM(settings=settings)

    if settings.LLM_PROVIDER == "groq":
        return GroqLLM(settings=settings)

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")
