from unittest.mock import Mock, patch

import pytest
import requests

from app.config.settings import Settings
from app.llm.exceptions import LLMGenerationError
from app.llm.ollama import OllamaLLM
from app.schemas.prompt import Prompt


def create_prompt():
    return Prompt(
        system_prompt="You are an engineering assistant.",
        user_prompt="How does Kafka authentication work?",
    )


def create_settings():
    return Settings(
        OLLAMA_BASE_URL="http://test-ollama:11434",
        OLLAMA_MODEL="test-model",
    )


@patch("app.llm.ollama.requests.post")
def test_ollama_generate(mock_post):
    mock_response = Mock()

    mock_response.json.return_value = {
        "response": "Kafka uses SASL for authentication."
    }

    mock_post.return_value = mock_response

    llm = OllamaLLM(settings=create_settings())

    result = llm.generate(create_prompt())

    assert result == "Kafka uses SASL for authentication."

    mock_post.assert_called_once_with(
        "http://test-ollama:11434/api/generate",
        json={
            "model": "test-model",
            "system": "You are an engineering assistant.",
            "prompt": "How does Kafka authentication work?",
            "stream": False,
        },
        timeout=60,
    )


@patch("app.llm.ollama.requests.post")
def test_ollama_http_error(mock_post):
    mock_post.side_effect = requests.RequestException("Connection failed")

    llm = OllamaLLM(settings=create_settings())

    with pytest.raises(
        LLMGenerationError,
        match="Failed to generate response",
    ):
        llm.generate(create_prompt())


@patch("app.llm.ollama.requests.post")
def test_ollama_invalid_json(mock_post):
    mock_response = Mock()

    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON")

    mock_post.return_value = mock_response

    llm = OllamaLLM(settings=create_settings())

    with pytest.raises(
        LLMGenerationError,
        match="Invalid response",
    ):
        llm.generate(create_prompt())


@patch("app.llm.ollama.requests.post")
def test_ollama_missing_response(mock_post):
    mock_response = Mock()

    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}

    mock_post.return_value = mock_response

    llm = OllamaLLM(settings=create_settings())

    with pytest.raises(
        LLMGenerationError,
        match="Invalid response",
    ):
        llm.generate(create_prompt())
