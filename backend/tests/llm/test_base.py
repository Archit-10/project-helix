from collections.abc import Iterator

import pytest

from app.llm.base import LLM
from app.schemas.prompt import Prompt


def test_llm_is_abstract():
    with pytest.raises(TypeError):
        LLM()


def test_llm_generate_is_abstract():
    class TestLLM(LLM):
        def generate(self, prompt: Prompt) -> str:
            return "test response"

        def generate_stream(self, prompt: Prompt) -> Iterator[str]:
            yield "test response"

    llm = TestLLM()

    prompt = Prompt(
        system_prompt="You are a test assistant.",
        user_prompt="Hello",
    )

    assert llm.generate(prompt) == "test response"
