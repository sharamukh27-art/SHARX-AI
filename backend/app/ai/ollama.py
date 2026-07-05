"""Ollama AI Provider Implementation"""

import httpx
import logging
from typing import List, AsyncGenerator
from .base import AIProvider, Message

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    """Ollama local model provider"""
    
    def __init__(self, base_url: str, model: str):
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Base URL of Ollama server (e.g., http://localhost:11434)
            model: Model name to use (e.g., neural-chat)
        """
        self.base_url = base_url.rstrip("/")
        self._model = model
        self.client = httpx.AsyncClient(timeout=300.0)
    
    async def chat(self, messages: List[Message], **kwargs) -> str:
        """
        Send a chat message to Ollama and get response.
        
        Args:
            messages: List of messages
            **kwargs: Additional arguments (temperature, top_p, etc.)
        
        Returns:
            Response text
        """
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": kwargs
        }
        
        try:
            response = await self.client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            raise
    
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream chat response from Ollama.
        
        Args:
            messages: List of messages
            **kwargs: Additional arguments
        
        Yields:
            Chunks of response text
        """
        payload = {
            "model": self._model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            "options": kwargs
        }
        
        try:
            async with self.client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            import json
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except Exception as e:
                            logger.error(f"Error parsing Ollama stream: {e}")
        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Ollama server is available"""
        try:
            response = await self.client.get(f"{self.base_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False
    
    @property
    def model_name(self) -> str:
        """Get model name"""
        return self._model
