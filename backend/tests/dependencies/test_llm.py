from app.config.settings import get_settings
from app.dependencies.llm import get_llm
from app.llm.ollama import OllamaLLM


def test_get_llm():
    llm = get_llm()

    assert isinstance(llm, OllamaLLM)
    assert llm.model == get_settings().OLLAMA_MODEL
    assert llm.base_url == get_settings().OLLAMA_BASE_URL
