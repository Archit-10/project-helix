import json
from collections.abc import Iterator

import requests

from app.config.settings import Settings
from app.llm.base import LLM
from app.llm.exceptions import LLMGenerationError
from app.schemas.prompt import Prompt


class OllamaLLM(LLM):
    def __init__(self, settings: Settings):
        self.model = settings.OLLAMA_MODEL
        self.base_url = settings.OLLAMA_BASE_URL

    def generate(self, prompt: Prompt) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "system": prompt.system_prompt,
                    "prompt": prompt.user_prompt,
                    "stream": False,
                },
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            return data["response"]

        except requests.RequestException as exc:
            raise LLMGenerationError("Failed to generate response from Ollama") from exc

        except (ValueError, KeyError) as exc:
            raise LLMGenerationError("Invalid response received from Ollama") from exc

    def generate_stream(self, prompt: Prompt) -> Iterator[str]:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "system": prompt.system_prompt,
                    "prompt": prompt.user_prompt,
                    "stream": True,
                },
                stream=True,
                timeout=60,
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                data = json.loads(line)

                yield data["response"]

        except requests.RequestException as exc:
            raise LLMGenerationError("Failed to generate response from Ollama") from exc

        except (ValueError, KeyError) as exc:
            raise LLMGenerationError("Invalid response received from Ollama") from exc
