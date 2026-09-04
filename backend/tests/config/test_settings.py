from app.config.settings import Settings


def test_ollama_settings_defaults():
    settings = Settings()

    assert settings.OLLAMA_BASE_URL == "http://localhost:11434"
    assert settings.OLLAMA_MODEL == "qwen2.5:3b"
