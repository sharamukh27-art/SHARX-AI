"""OpenAI AI Provider Implementation"""

import httpx
import logging
from typing import List, AsyncGenerator
from .base import AIProvider, Message

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""

    def __init__(self, api_key: str, model: str):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name to use (e.g., gpt-4-turbo-preview)
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self._api_key = api_key
        self._model = model
        self.api_url = "https://api.openai.com/v1"
        self.client = httpx.AsyncClient(
            timeout=300.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

    async def chat(self, messages: List[Message], **kwargs) -> str:
        """
        Send a chat message to OpenAI and get response.

        Args:
            messages: List of messages
            **kwargs: Additional arguments (temperature, top_p, etc.)

        Returns:
            Response text
        """
        try:
            payload = {
                "model": self._model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                **kwargs,
            }
            response = await self.client.post(f"{self.api_url}/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise

    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream chat response from OpenAI.

        Args:
            messages: List of messages
            **kwargs: Additional arguments

        Yields:
            Chunks of response text
        """
        try:
            payload = {
                "model": self._model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "stream": True,
                **kwargs,
            }
            async with self.client.stream("POST", f"{self.api_url}/chat/completions", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    line = line.removeprefix("data:").strip()
                    if line == "[DONE]":
                        break
                    try:
                        import json
                        chunk_data = json.loads(line)
                    except Exception:
                        continue
                    delta = chunk_data.get("choices", [])[0].get("delta", {}).get("content")
                    if delta:
                        yield delta
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise

    async def health_check(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            response = await self.client.get(f"{self.api_url}/models")
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"OpenAI health check failed: {e}")
            return False

    @property
    def model_name(self) -> str:
        """Get model name"""
        return self._model
