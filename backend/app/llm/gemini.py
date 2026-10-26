import json
from collections.abc import Iterator

import requests

from app.config.settings import Settings
from app.llm.base import LLM
from app.llm.exceptions import LLMGenerationError
from app.schemas.prompt import Prompt


class GeminiLLM(LLM):
    def __init__(self, settings: Settings):
        self.model = settings.GEMINI_MODEL
        self.base_url = settings.GEMINI_BASE_URL.rstrip("/")
        self.api_key = settings.GEMINI_API_KEY

        if not self.api_key.strip():
            raise LLMGenerationError(
                "GEMINI_API_KEY is required when using the Gemini provider"
            )

    def _request(self, prompt: Prompt, stream: bool = False):
        return requests.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt.system_prompt},
                    {"role": "user", "content": prompt.user_prompt},
                ],
                "stream": stream,
            },
            stream=stream,
            timeout=60,
        )

    def generate(self, prompt: Prompt) -> str:
        try:
            response = self._request(prompt)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]

            if not isinstance(content, str):
                raise ValueError("Missing assistant message content")

            return content

        except requests.RequestException as exc:
            raise LLMGenerationError("Failed to generate response from Gemini") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise LLMGenerationError("Invalid response received from Gemini") from exc

    def generate_stream(self, prompt: Prompt) -> Iterator[str]:
        response = None

        try:
            response = self._request(prompt, stream=True)
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                if isinstance(line, bytes):
                    line = line.decode("utf-8")

                if not line.startswith("data:"):
                    continue

                data_line = line[len("data:") :].strip()
                if data_line == "[DONE]":
                    break

                data = json.loads(data_line)
                choices = data["choices"]
                if not choices:
                    continue

                content = choices[0].get("delta", {}).get("content")
                if content:
                    yield content

        except requests.RequestException as exc:
            raise LLMGenerationError("Failed to generate response from Gemini") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise LLMGenerationError("Invalid response received from Gemini") from exc
        finally:
            if response is not None:
                response.close()
