from unittest.mock import Mock

import pytest
import requests

from app.config.settings import Settings
from app.llm.exceptions import LLMGenerationError
from app.llm.groq import GroqLLM
from app.schemas.prompt import Prompt


@pytest.fixture
def settings():
    return Settings(
        GROQ_API_KEY="test-api-key",
        GROQ_BASE_URL="https://api.groq.com/openai/v1",
        GROQ_MODEL="test-model",
    )


@pytest.fixture
def prompt():
    return Prompt(
        system_prompt="You are a helpful assistant.",
        user_prompt="What is hybrid retrieval?",
    )


def test_groq_generate(monkeypatch, settings, prompt):
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [
            {"message": {"content": "Hybrid retrieval combines search methods."}}
        ]
    }
    monkeypatch.setattr(requests, "post", Mock(return_value=mock_response))

    llm = GroqLLM(settings)
    result = llm.generate(prompt)

    assert result == "Hybrid retrieval combines search methods."

    args, kwargs = requests.post.call_args
    assert args[0] == "https://api.groq.com/openai/v1/chat/completions"
    assert kwargs["headers"]["Authorization"] == "Bearer test-api-key"
    assert kwargs["json"]["model"] == "test-model"
    assert kwargs["json"]["stream"] is False
    assert kwargs["json"]["messages"] == [
        {"role": "system", "content": prompt.system_prompt},
        {"role": "user", "content": prompt.user_prompt},
    ]
    mock_response.raise_for_status.assert_called_once()


def test_groq_generate_http_error(monkeypatch, settings, prompt):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Unauthorized")
    monkeypatch.setattr(requests, "post", Mock(return_value=mock_response))

    with pytest.raises(
        LLMGenerationError, match="Failed to generate response from Groq"
    ):
        GroqLLM(settings).generate(prompt)


def test_groq_generate_invalid_response(monkeypatch, settings, prompt):
    mock_response = Mock()
    mock_response.json.return_value = {"choices": []}
    monkeypatch.setattr(requests, "post", Mock(return_value=mock_response))

    with pytest.raises(LLMGenerationError, match="Invalid response received from Groq"):
        GroqLLM(settings).generate(prompt)


def test_groq_generate_stream(monkeypatch, settings, prompt):
    lines = [
        b'data: {"choices":[{"delta":{"content":"Hybrid "}}]}',
        b'data: {"choices":[{"delta":{"content":"retrieval"}}]}',
        b'data: {"choices":[{"delta":{}}]}',
        b"data: [DONE]",
    ]

    mock_response = Mock()
    mock_response.iter_lines.return_value = iter(lines)
    monkeypatch.setattr(requests, "post", Mock(return_value=mock_response))

    llm = GroqLLM(settings)
    result = list(llm.generate_stream(prompt))

    assert result == ["Hybrid ", "retrieval"]

    _, kwargs = requests.post.call_args
    assert kwargs["stream"] is True
    mock_response.raise_for_status.assert_called_once()
    mock_response.close.assert_called_once()


def test_groq_generate_stream_invalid_json(monkeypatch, settings, prompt):
    mock_response = Mock()
    mock_response.iter_lines.return_value = iter([b"data: {invalid-json}"])
    monkeypatch.setattr(requests, "post", Mock(return_value=mock_response))

    with pytest.raises(LLMGenerationError, match="Invalid response received from Groq"):
        list(GroqLLM(settings).generate_stream(prompt))

    mock_response.close.assert_called_once()


def test_groq_requires_api_key():
    settings = Settings(GROQ_API_KEY="")

    with pytest.raises(LLMGenerationError, match="GROQ_API_KEY is required"):
        GroqLLM(settings)
