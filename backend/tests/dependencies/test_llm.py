from app.config.settings import Settings
from app.dependencies.llm import get_llm
from app.llm.groq import GroqLLM
from app.llm.ollama import OllamaLLM


def test_get_llm_ollama(monkeypatch):
    settings = Settings(LLM_PROVIDER="ollama")

    monkeypatch.setattr(
        "app.dependencies.llm.get_settings",
        lambda: settings,
    )
    get_llm.cache_clear()

    try:
        llm = get_llm()

        assert isinstance(llm, OllamaLLM)
        assert llm.model == settings.OLLAMA_MODEL
        assert llm.base_url == settings.OLLAMA_BASE_URL
    finally:
        get_llm.cache_clear()


def test_get_llm_groq(monkeypatch):
    settings = Settings(
        LLM_PROVIDER="groq",
        GROQ_API_KEY="test-api-key",
    )

    monkeypatch.setattr(
        "app.dependencies.llm.get_settings",
        lambda: settings,
    )
    get_llm.cache_clear()

    try:
        llm = get_llm()

        assert isinstance(llm, GroqLLM)
        assert llm.model == settings.GROQ_MODEL
        assert llm.base_url == settings.GROQ_BASE_URL
    finally:
        get_llm.cache_clear()


def test_default_provider_is_ollama():
    assert Settings.model_fields["LLM_PROVIDER"].default == "ollama"
