from abc import ABC, abstractmethod
from collections.abc import Iterator

from app.schemas.prompt import Prompt


class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: Prompt) -> str:
        pass

    @abstractmethod
    def generate_stream(self, prompt: Prompt) -> Iterator[str]:
        pass
